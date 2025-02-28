from flask import Flask, request, jsonify, render_template
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from database import initialize_db, save_review, save_conversation, get_recent_reviews, get_conversations, delete_review
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

groq_api_key = os.getenv("GROQ_API_KEY")


# Initialize Groq client
llm = ChatGroq(
    api_key=groq_api_key,
    model_name="mixtral-8x7b-32768"
)

# Initialize conversation memory
memories = {}

def get_or_create_memory(review_id):
    if review_id not in memories:
        memories[review_id] = ConversationBufferWindowMemory(
            k=5,  # Keep last 5 interactions
            return_messages=True,
            memory_key="chat_history",
        )
    return memories[review_id]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/review', methods=['POST'])
def review_code():
    data = request.json
    code = data.get('code')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    # Create the conversation chain with memory
    memory = ConversationBufferWindowMemory(
        k=5,
        return_messages=True,
        memory_key="chat_history",
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional code reviewer. Analyze the code and provide detailed feedback."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", """Please review the following code and provide detailed feedback:
        
        {input}
        
        Please analyze:
        1. Code quality and style
        2. Potential bugs or issues
        3. Performance considerations
        4. Security concerns
        5. Suggestions for improvement""")
    ])

    conversation = ConversationChain(
        memory=memory,
        prompt=prompt,
        llm=llm,
    )
    
    # Generate the review
    review = conversation.predict(input=code)
    
    # Save to database
    saved_review = save_review(code, review)
    
    # Initialize memory for this review
    memories[saved_review.id] = memory
    
    return jsonify({
        'review_id': saved_review.id,
        'review': review
    })

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    review_id = data.get('review_id')
    question = data.get('question')
    
    if not review_id or not question:
        return jsonify({'error': 'Missing review_id or question'}), 400
    
    # Get the memory for this review
    memory = get_or_create_memory(review_id)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful code assistant. Use the conversation history to provide context-aware responses."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    
    conversation = ConversationChain(
        memory=memory,
        prompt=prompt,
        llm=llm,
    )
    
    # Generate response with context
    answer = conversation.predict(input=question)
    
    # Save conversation to database
    save_conversation(review_id, question, answer)
    
    return jsonify({'answer': answer})

@app.route('/history', methods=['GET'])
def get_history():
    reviews = get_recent_reviews()
    history = []
    
    for review in reviews:
        conversations = get_conversations(review.id)
        history.append({
            'id': review.id,
            'code': review.code,
            'review': review.review,
            'created_at': review.created_at.isoformat(),
            'conversations': [{
                'question': conv.question,
                'answer': conv.answer,
                'created_at': conv.created_at.isoformat()
            } for conv in conversations]
        })
    
    return jsonify(history)

@app.route('/delete/<int:review_id>', methods=['DELETE'])
def delete_review_endpoint(review_id):
    try:
        delete_review(review_id)
        if review_id in memories:
            del memories[review_id]
        return jsonify({'message': 'Review deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)
