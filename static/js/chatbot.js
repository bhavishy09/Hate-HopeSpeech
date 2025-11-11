document.addEventListener('DOMContentLoaded', function() {
    const chatbotMessagesRect = document.getElementById('chatbotMessagesRect');
    const quickActionBtnsRect = document.querySelectorAll('.quick-action-btn-rect');
    
    const responses = {
        'video-id': "To find a YouTube video ID:\n\n1. Open the YouTube video in your browser\n2. Look at the URL: youtube.com/watch?v=VIDEO_ID\n3. The video ID is the text after 'v=' (usually 11 characters)\n4. For example: in 'youtube.com/watch?v=dQw4w9WgXcQ', the ID is 'dQw4w9WgXcQ'\n\nJust copy that ID and paste it into the prediction form above!",
        
        'sentiment': "Our AI analyzes comments and categorizes them into three sentiments:\n\n🟢 Positive: Supportive, happy, or encouraging comments that spread hope\n\n🟡 Neutral: Factual or neutral comments without strong emotions\n\n🔴 Negative: Critical, hateful, or discouraging comments\n\nThis helps you understand the overall tone of your video's comments!",
        
        'accuracy': "Our sentiment analysis uses advanced AI algorithms to provide accurate predictions. However, please note:\n\n✓ This is currently a demonstration with a placeholder model\n✓ Real-world accuracy depends on the ML model integration\n✓ Context and sarcasm can sometimes be challenging for AI\n✓ Results are meant to give you general insights into comment sentiment\n\nWe're constantly working to improve accuracy!",
        
        'usage': "Here's how to use CommentIQ:\n\n1️⃣ Sign up for a free account\n2️⃣ Go to the Predict page\n3️⃣ Enter a YouTube video ID\n4️⃣ Click 'Analyze Sentiment'\n5️⃣ View your results instantly!\n6️⃣ Check your Dashboard to see prediction history and analytics\n\nIt's that simple! Start understanding your audience better today."
    };
    
    function addMessage(message, isBot = true) {
        if (!chatbotMessagesRect) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${isBot ? 'bot' : 'user'}`;
        messageDiv.textContent = message;
        messageDiv.style.whiteSpace = 'pre-line';
        chatbotMessagesRect.appendChild(messageDiv);
        chatbotMessagesRect.scrollTop = chatbotMessagesRect.scrollHeight;
    }
    
    if (quickActionBtnsRect) {
        quickActionBtnsRect.forEach(btn => {
            btn.addEventListener('click', function() {
                const question = this.getAttribute('data-question');
                const questionText = this.textContent;
                
                addMessage(questionText, false);
                
                setTimeout(() => {
                    const response = responses[question];
                    if (response) {
                        addMessage(response, true);
                    }
                }, 500);
            });
        });
    }
});
