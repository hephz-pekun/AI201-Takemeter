import gradio as gr
import torch

def predict_book_post(text):
    inputs = tokenizer(
        text,
        truncation=True,
        max_length=256,
        return_tensors="pt"
    )

    model.eval()

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(
            outputs.logits,
            dim=-1
        )

    pred_id = torch.argmax(probs).item()

    label = ID_TO_LABEL[pred_id]
    confidence = probs[0][pred_id].item()

    return f"{label} ({confidence:.2%} confidence)"

demo = gr.Interface(
    fn=predict_book_post,
    inputs=gr.Textbox(
        lines=6,
        label="Book Discussion Post"
    ),
    outputs=gr.Textbox(
        label="Predicted Category"
    ),
    title="Book Discussion Classifier",
    description="""
Classifies r/books posts into one of four categories:

• Recommendation
• Review
• Literary_Analysis
• Publishing_and_Book_Info
"""
)

demo.launch()