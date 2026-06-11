import os
import ollama
from flask import Flask, request, jsonify
from search_engine import smart_search
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def generate_llm_answer(query, contexts):
    """
    Takes the 3 precision contexts and uses local Llama 
    to synthesize them into one single, cohesive paragraph.
    """
    # Combine our 3 separate chunks into one block of reference data
    combined_context = "\n---\n".join(contexts)
    
    system_prompt = (
        "You are a precise, professional document assistant. Answer the user's question "
        "by summarizing the provided context snippets into ONE single, concise paragraph. "
        "Do not list out separate matches or use bullet points. Blend the information "
        "naturally and use only the facts provided."
    )
    
    user_prompt = f"Context files:\n{combined_context}\n\nQuestion: {query}"
    
    try:
        print("-> Stage 3: Synthesizing final answer using local Llama...")
        response = ollama.chat(
            model='llama3.2',  # Change to 'llama3.1' if you downloaded that instead
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"[Local LLM Error: {e}] Failed to synthesize. Raw chunks: {combined_context}"


@app.route("/api/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Please provide a 'question' key in the JSON request body."}), 400
        
    user_query = data["question"]
    
    try:
        # Step 1 & 2: Get the precision context chunks
        top_contexts = smart_search(user_query)
        
        if not top_contexts:
            return jsonify({
                "query": user_query,
                "answer": "No relevant documentation found in the database.",
                "context_used": []
            })
            
        # Step 3: Synthesize the final conversational answer
        final_answer = generate_llm_answer(user_query, top_contexts)
        
        return jsonify({
            "query": user_query,
            "answer": final_answer,
            "context_used": top_contexts
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("\nStarting Two-Stage FAQ Assistant API Server...")
    # use_reloader=False prevents heavy ML models from doubling up in your 16GB RAM
    app.run(debug=True, port=5000, use_reloader=False)