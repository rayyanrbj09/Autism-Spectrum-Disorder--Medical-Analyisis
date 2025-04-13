# visualizer.py
import streamlit as st
import matplotlib.pyplot as plt
import logging

logging.basicConfig(filename='asd_app.log', level=logging.DEBUG)

def plot_qchat_score(score):
    """
    Plot a horizontal bar chart for Q-Chat score visualization.
    """
    logging.debug("Rendering Q-Chat score plot")
    try:
        fig, ax = plt.subplots(figsize=(8, 1.5))
        colors = ['green' if i <= 3 else 'orange' if i <= 6 else 'red' for i in range(11)]
        for i in range(11):
            ax.barh(0, 1, left=i, color=colors[i])
        ax.axvline(score, color='blue', linestyle='--', linewidth=2)
        ax.set_yticks([])
        ax.set_xticks(range(11))
        ax.set_title("Q-Chat-10 Score Visualization")
        st.pyplot(fig)
        plt.close(fig)  # Free memory
        logging.debug("Plot rendered successfully")
    except Exception as e:
        logging.error(f"Failed to render plot: {e}")
        st.warning(f"Failed to render plot: {e}")