
"""
NEXT WORD NOTEBOOK (Gradio Web App)

Run:
    python predictor_app.py

Then open:
    http://127.0.0.1:7860

Keep this file in the same folder as predictor.py.
"""

import gradio as gr
import predictor_app as se


TEST_WORDS = getattr(se, "TEST_WORDS", [])


def probabilities(word):
    counts = se.BIGRAMS.get(word, {})
    total = sum(counts.values())

    if total == 0:
        return {}

    return {
        following: count / total
        for following, count in counts.items()
    }



def predict(word):
    chances = probabilities(word.lower().strip())

    if not chances:
        return {"the": 1.0}

    return chances

def test_model():
    mistakes = 0
    results = []

    for word, wanted in TEST_WORDS:
        answer = max(predict(word), key=predict(word).get)

        if answer != wanted:
            mistakes += 1

        results.append(
            f"{word} → {answer} | Expected: {wanted}"
        )

    results.append(
        f"\nMistakes: {mistakes} out of {len(TEST_WORDS)}"
    )

    return "\n".join(results)


def write(word, length):
    current = word.lower().strip() or "the"
    output = [current]

    for _ in range(int(length)):
        next_words = probabilities(current)

        if not next_words:
            current = "the"
        else:
            current = max(
                next_words,
                key=next_words.get
            )

        output.append(current)

    return " ".join(output)


with gr.Blocks(title="Next Word Notebook") as demo:

    gr.Markdown(
        """
        # NEXT WORD NOTEBOOK

        ### A Simple Next Word Prediction Model

        Type a word and see what the model predicts next.
        """
    )

    with gr.Row():
        word = gr.Textbox(
            label="Enter a word",
            value="the",
            placeholder="Type a word..."
        )

        predict_button = gr.Button("Predict Next Word")

    bars = gr.Label(
        label="Next Word Probabilities",
        num_top_classes=5
    )

    predict_button.click(
        predict,
        inputs=word,
        outputs=bars
    )

    word.change(
        predict,
        inputs=word,
        outputs=bars
    )

    gr.Markdown("## Generate Text")

    with gr.Row():
        start = gr.Textbox(
            label="Starting word",
            value="the"
        )

        length = gr.Slider(
            minimum=1,
            maximum=50,
            value=10,
            step=1,
            label="Number of words"
        )

    generate_button = gr.Button("Generate Text")

    story = gr.Textbox(
        label="Generated Text",
        lines=4
    )

    generate_button.click(
        write,
        inputs=[start, length],
        outputs=story
    )

    gr.Markdown("## Test the Model")

    test_button = gr.Button("Run All Tests")

    results = gr.Textbox(
        label="Test Results",
        lines=8
    )

    test_button.click(
        test_model,
        inputs=[],
        outputs=results
    )

    gr.Markdown(
        """
        ---
        **Project:** Next Word Notebook

        **Method:** Bigram probability model

        **Purpose:** Predict the next word using training text.
        """
    )

if __name__ == "__main__":
    demo.launch()
