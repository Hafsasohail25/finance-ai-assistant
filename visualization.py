import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 📊 1. Horizontal Bar Chart: Spending by Category
def plot_spending_chart(df):
    # Grouping by category and summing the amounts
    category_amounts = df.groupby("category")["amount"].sum().sort_values(ascending=True)

    # Create the figure with a minimal size and clean design
    fig, ax = plt.subplots(figsize=(5, 2))  # Adjusted size for neatness
    sns.set_style("whitegrid")

    bars = ax.barh(
        category_amounts.index,
        category_amounts.values,
        color=sns.color_palette("coolwarm", len(category_amounts)),
        edgecolor="black"
    )

    # Adding value annotations with smaller font and cleaner style
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height() / 2,
                f"${width:,.2f}", va="center", fontsize=8, color="black")  # Slightly larger font for clarity

    ax.set_xlabel("Amount Spent ($)", fontsize=9)  # Adjusted label font size
    ax.set_title("💰 Spending by Category", fontsize=10, weight="bold")  # Adjusted title size
    ax.spines["top"].set_visible(False)  # Removing unnecessary top spine
    ax.spines["right"].set_visible(False)  # Removing unnecessary right spine
    ax.spines["left"].set_linewidth(0.5)  # Making the left spine thinner for a cleaner look
    ax.spines["bottom"].set_linewidth(0.5)  # Same for the bottom
    plt.tight_layout()  # Ensures everything fits neatly

    return fig

# 📊 Plotting the Monthly Trend
def plot_monthly_trend(df):
    # Ensure the 'date' column is in datetime format
    df['month'] = df['date'].dt.to_period('M')  # Extract year and month
    
    # Group by month and calculate the sum of amounts
    monthly_data = df.groupby('month')['amount'].sum()

    # Create a clean, compact line chart for the monthly trend
    fig, ax = plt.subplots(figsize=(6, 3))  # Adjusted size for a cleaner presentation
    ax.plot(monthly_data.index.astype(str), monthly_data.values, marker='o', linestyle='-', color='#6366f1')
    ax.set_xlabel('Month', fontsize=9)  # Adjusted x-axis label font size
    ax.set_ylabel('Total Amount Spent ($)', fontsize=9)  # Adjusted y-axis label font size
    ax.set_title('Monthly Spending Trend', fontsize=12)  # Adjusted title font size
    ax.grid(True, linestyle='--', alpha=0.5)  # Light grid lines for clarity

    plt.tight_layout()  # Ensures everything fits properly

    return fig
