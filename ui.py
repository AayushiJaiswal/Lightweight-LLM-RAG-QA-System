"""
ERP RAG UI - Cyberpunk Holographic Design (Final Corrected)
"""

import gradio as gr
import json
from datetime import datetime
from pathlib import Path


# Ultra Modern Custom CSS
CUSTOM_CSS = """
/* Animated Particle Background */
body {
    background: #0f0c29;
    background: linear-gradient(to right, #24243e, #302b63, #0f0c29);
    position: relative;
    overflow-x: hidden;
}

body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(252, 70, 107, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 40% 20%, rgba(45, 253, 255, 0.2) 0%, transparent 50%);
    animation: particle-float 15s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes particle-float {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 0.8; transform: scale(1.1); }
}

/* Glassmorphism Container */
.contain {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border-radius: 30px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 
        0 8px 32px 0 rgba(31, 38, 135, 0.37),
        inset 0 0 20px rgba(255, 255, 255, 0.05) !important;
    padding: 40px !important;
    position: relative;
    z-index: 1;
}

/* Holographic Header */
.holo-header {
    background: linear-gradient(
        135deg,
        #667eea 0%,
        #764ba2 25%,
        #f093fb 50%,
        #4facfe 75%,
        #00f2fe 100%
    );
    background-size: 400% 400%;
    animation: holo-shift 8s ease infinite;
    padding: 30px;
    border-radius: 25px;
    text-align: center;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.6);
}

.holo-header::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        45deg,
        transparent,
        rgba(255, 255, 255, 0.3),
        transparent
    );
    animation: shine 3s infinite;
}

@keyframes holo-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes shine {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

.holo-header h1 {
    color: white;
    font-size: 3rem;
    font-weight: 900;
    margin: 0;
    text-shadow: 
        0 0 10px rgba(255, 255, 255, 0.8),
        0 0 20px rgba(102, 126, 234, 0.6),
        0 0 30px rgba(102, 126, 234, 0.4);
    position: relative;
    z-index: 1;
}

/* Neon Input Box */
textarea, input {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 2px solid transparent !important;
    border-radius: 20px !important;
    padding: 20px !important;
    color: white !important;
    font-size: 16px !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 
        inset 2px 2px 5px rgba(0, 0, 0, 0.5),
        inset -2px -2px 5px rgba(255, 255, 255, 0.05) !important;
}

textarea:focus, input:focus {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 2px solid rgba(102, 126, 234, 0.8) !important;
    box-shadow: 
        0 0 20px rgba(102, 126, 234, 0.6),
        inset 0 0 10px rgba(102, 126, 234, 0.2) !important;
    transform: translateY(-2px);
}

/* 3D Button Effect */
button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 15px 35px !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
    transition: all 0.3s ease !important;
    box-shadow: 
        0 8px 20px rgba(102, 126, 234, 0.4),
        inset 0 0 10px rgba(255, 255, 255, 0.2) !important;
}

button:hover {
    transform: translateY(-5px) scale(1.05) !important;
    box-shadow: 
        0 15px 40px rgba(102, 126, 234, 0.6),
        inset 0 0 20px rgba(255, 255, 255, 0.3) !important;
}

/* Floating Card Effect */
.floating-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 25px;
    margin: 20px 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 
        0 10px 30px rgba(0, 0, 0, 0.3),
        inset 0 0 15px rgba(255, 255, 255, 0.05);
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

/* Cyberpunk Example Items */
.cyber-example {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
    border-left: 3px solid #667eea;
    border-radius: 15px;
    padding: 15px 20px;
    margin: 10px 0;
    color: #e0e0e0;
    cursor: pointer;
    transition: all 0.3s ease;
}

.cyber-example:hover {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
    border-left-width: 6px;
    transform: translateX(10px);
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}

/* Holographic Stats Badges */
.holo-badge {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
    background-size: 200% 200%;
    animation: holo-badge 3s ease infinite;
    padding: 12px 24px;
    border-radius: 25px;
    color: white;
    font-weight: 700;
    margin: 8px;
    box-shadow: 
        0 5px 15px rgba(102, 126, 234, 0.4),
        inset 0 0 10px rgba(255, 255, 255, 0.2);
}

@keyframes holo-badge {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Feedback Section */
.neon-section {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 25px;
    padding: 30px;
    margin-top: 30px;
    border: 2px solid rgba(102, 126, 234, 0.3);
    box-shadow: 
        0 0 30px rgba(102, 126, 234, 0.3),
        inset 0 0 20px rgba(102, 126, 234, 0.1);
}

/* Text Styling */
h1, h2, h3, h4 {
    color: #e0e0e0 !important;
    text-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
}

p, span, label {
    color: #b0b0b0 !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 10px;
}
"""


class RAGInterface:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.feedback_log = []
        self.query_count = 0

    def respond(self, message, history):
        if not message or not message.strip():
            return ""

        self.query_count += 1

        try:
            result = self.pipeline.answer_question(message, top_k=3)

            response = "### 🌟 SYSTEM RESPONSE\n\n"
            response += f"> {result.get('answer', 'No data found')}\n\n"
            response += "---\n\n### 📡 DATA SOURCES\n\n"

            for i, source in enumerate(result.get("sources", []), 1):
                score = source.get("score", 0)
                emoji = "🟢 HIGH" if score > 0.7 else "🟡 MEDIUM" if score > 0.5 else "🔴 LOW"
                
                response += f"**[{i}] {source.get('source', 'Unknown')}**\n"
                response += f"├─ Confidence: {emoji} ({score:.1%})\n"
                response += f"└─ `{source.get('text', '')[:100]}...`\n\n"

            confidence = result.get("confidence", 0)
            response += "\n---\n"
            response += f"🔢 **QUERY ID:** #{self.query_count} | "
            response += f"📊 **ACCURACY:** {confidence:.1%} | "
            response += f"🤖 **ENGINE:** Ollama-3.2"

        except Exception as e:
            response = (
                "### ⚠️ SYSTEM ERROR\n\n"
                f"```\n{str(e)}\n```\n\n"
                "**RECOVERY STEPS:**\n"
                "1. Initialize: `ollama serve`\n"
                "2. Verify: `ollama list`\n"
                "3. Test: `ollama run llama3.2`"
            )

        return response

    def save_feedback(self, rating, comment):
        feedback = {
            "timestamp": datetime.now().isoformat(),
            "rating": int(rating),
            "comment": comment,
            "query_id": self.query_count,
        }

        self.feedback_log.append(feedback)
        Path("data/feedback").mkdir(parents=True, exist_ok=True)

        with open("data/feedback/feedback.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(feedback) + "\n")

        avg = sum(f["rating"] for f in self.feedback_log) / len(self.feedback_log)
        
        # Return success message AND clear inputs
        return (
            f"✨ FEEDBACK LOGGED | Rating: {rating}⭐ | Avg: {avg:.1f}⭐",
            5,  # Reset rating slider to 5
            ""  # Clear comment textbox
        )

    def launch(self, port=7860):

        with gr.Blocks(title="ERP Intelligence") as demo:

            # Header
            gr.HTML("""
                <div class="holo-header">
                    <h1>⚡ ERP INTELLIGENCE MATRIX ⚡</h1>
                    <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 15px; font-weight: 600;">
                        🔮 Neural Network • 🚀 Quantum Speed • 🛡️ Ultra Secure
                    </p>
                </div>
            """)

            # Main Layout
            with gr.Row():
                # Left Column - Chat
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(
                        label="",
                        height=450
                    )

                    msg = gr.Textbox(
                        label="Your Question",
                        placeholder="Ask ERP intelligence...",
                        lines=1
                    )

                    send_btn = gr.Button("🚀 ASK", variant="primary")

                    # Chat function
                    def send_message(message, history):
                        if not message:
                            return "", history
                        
                        if history is None:
                            history = []

                        # Get response
                        response = self.respond(message, history)

                        # Append to history
                        history.append({"role": "user", "content": message})
                        history.append({"role": "assistant", "content": response})

                        return "", history

                    send_btn.click(send_message, [msg, chatbot], [msg, chatbot])
                    msg.submit(send_message, [msg, chatbot], [msg, chatbot])

                # Right Column - Examples & Feedback
                with gr.Column(scale=2):
                    # Examples
                    gr.HTML("""
                        <div class="floating-card">
                            <h3 style="color:#667eea;margin-bottom:20px;">
                                💫 QUICK ACCESS COMMANDS
                            </h3>
                            <div class="cyber-example">🔹 Purchase order workflow</div>
                            <div class="cyber-example">🔹 Expense validation protocol</div>
                            <div class="cyber-example">🔹 Vendor registration</div>
                            <div class="cyber-example">🔹 Payment processing</div>
                            <div class="cyber-example">🔹 Invoice verification</div>
                        </div>
                    """)

                    # Feedback Section
                    gr.HTML('<div class="neon-section">')
                    gr.Markdown("### 🌟 SYSTEM FEEDBACK")

                    rating = gr.Slider(1, 5, 5, step=1, label="⭐ QUALITY RATING")
                    comment = gr.Textbox(
                        label="💬 FEEDBACK",
                        placeholder="Enter feedback...",
                        lines=2
                    )

                    feedback_btn = gr.Button("📡 TRANSMIT", variant="primary")
                    status = gr.Textbox(show_label=False, interactive=False)

                    # Feedback submission with auto-clear
                    feedback_btn.click(
                        self.save_feedback,
                        inputs=[rating, comment],
                        outputs=[status, rating, comment]
                    )

                    gr.HTML("</div>")

            # Stats Badges
            gr.HTML("""
                <div style="margin-top:40px;text-align:center;">
                    <div class="holo-badge">🤖 AI-POWERED</div>
                    <div class="holo-badge">💎 ZERO-COST</div>
                    <div class="holo-badge">🔐 ENCRYPTED</div>
                    <div class="holo-badge">⚡ REAL-TIME</div>
                    <div class="holo-badge">🌐 OFFLINE-MODE</div>
                </div>
            """)

            # Footer
            gr.HTML("""
                <div style="margin-top:40px;padding:25px;background:rgba(102,126,234,0.1);
                            border-radius:20px;border:1px solid rgba(102,126,234,0.3);
                            text-align:center;">
                    <p style="color:#667eea;font-size:1.1rem;font-weight:600;">
                        🚀 POWERED BY OLLAMA NEURAL ENGINE
                    </p>
                    <p style="color:#888;">
                        🎨 Holographic Interface v2.0 • 🔐 Local Processing
                    </p>
                    <p style="color:#555;font-size:0.9rem;">
                        © 2025 ERP Intelligence Matrix
                    </p>
                </div>
            """)

        print("\n" + "⚡" * 40)
        print("🔮 ERP INTELLIGENCE MATRIX ONLINE 🔮".center(80))
        print("⚡" * 40)
        print(f"\n🌐 NEURAL LINK: http://localhost:{port}")
        print("💡 SHUTDOWN: Ctrl+C\n")
        print("=" * 80 + "\n")

        demo.launch(
            server_port=port,
            server_name="0.0.0.0",
            share=False,
            css=CUSTOM_CSS
        )


if __name__ == "__main__":
    print("▶️ INITIALIZE: python quick_start.py demo")