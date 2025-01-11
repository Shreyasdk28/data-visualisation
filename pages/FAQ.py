import streamlit as st

# Expanded sample FAQ data (could be loaded from a database or file)
faq_data = {
    "General": [
        {"question": "What is insurance?", "answer": "Insurance is a contract in which an individual or entity receives financial protection against losses."},
        {"question": "How does insurance work?", "answer": "Insurance works by pooling the risks of policyholders, where premiums paid by policyholders are used to cover the claims."},
        {"question": "What are the different types of insurance?", "answer": "The most common types of insurance include life, health, auto, home, and disability insurance."},
        {"question": "Can insurance premiums be refunded?", "answer": "In some cases, premiums may be refunded or partially refunded depending on the type of policy and insurer's terms."},
        {"question": "What is the role of an insurance agent?", "answer": "An insurance agent helps clients choose the right policy based on their needs and assists with filing claims."}
    ],
    "Policies": [
        {"question": "What types of insurance policies are available?", "answer": "There are many types of insurance policies, including life, health, auto, and home insurance."},
        {"question": "How do I purchase an insurance policy?", "answer": "You can purchase an insurance policy online, through an agent, or directly through an insurance company."},
        {"question": "What is the difference between term life and whole life insurance?", "answer": "Term life insurance provides coverage for a specific period, while whole life insurance provides lifetime coverage and builds cash value."},
        {"question": "How do I know which policy is right for me?", "answer": "It depends on your personal needs, budget, and goals. Consider consulting with an insurance agent to find the best option."},
        {"question": "Can I change my policy after purchase?", "answer": "Yes, many insurance companies allow you to modify your policy if your needs change. Be sure to consult with your insurer."}
    ],
    "Claims": [
        {"question": "How can I file a claim?", "answer": "You can file a claim by contacting your insurance provider through their website or customer service number."},
        {"question": "What documents are required for filing a claim?", "answer": "Documents such as a claim form, policy details, and proof of loss may be required."},
        {"question": "How long does it take to process a claim?", "answer": "Claim processing time varies depending on the insurance company and type of claim. It can take anywhere from a few days to several weeks."},
        {"question": "Can I track the status of my claim?", "answer": "Yes, most insurance companies provide online portals where you can check the status of your claim."},
        {"question": "What happens if my claim is denied?", "answer": "If your claim is denied, you can appeal the decision by providing additional evidence or contacting customer service for clarification."}
    ],
    "Investments": [
        {"question": "What is an investment in an insurance policy?", "answer": "An investment in insurance refers to the amount of money that you contribute towards your policy, which is then used to build your coverage."},
        {"question": "How can I track my investment returns?", "answer": "Investment returns can be tracked through your insurance company’s portal or via regular reports sent by your provider."},
        {"question": "What is a policyholder's equity?", "answer": "Policyholder's equity is the value of the insurance policy that accumulates over time through investments made by the insurance company."},
        {"question": "What are the risks associated with insurance investments?", "answer": "Insurance investments can be subject to market risks, and returns depend on the insurer’s investments and policy type."},
        {"question": "Can I change my investment allocation?", "answer": "In some cases, policyholders can modify their investment allocation depending on the type of policy and insurer’s offerings."}
    ]
}

# Function to display FAQ answers based on search query
def search_faq(query, category):
    results = []
    for faq in faq_data.get(category, []):
        if query.lower() in faq['question'].lower() or query.lower() in faq['answer'].lower():
            results.append(faq)
    return results

# Sidebar for category selection
category = st.sidebar.selectbox("Select a Category", ["General", "Policies", "Claims", "Investments"])

# Search bar to input search query
faq_search = st.text_input("Search for answers", "")

st.title("FAQ - Frequently Asked Questions")

if faq_search:
    st.write(f"Search Results for: {faq_search}")
    search_results = search_faq(faq_search, category)
    
    if search_results:
        for result in search_results:
            st.subheader(result["question"])
            st.write(result["answer"])
    else:
        st.write("No results found for your query.")
else:
    st.write("Browse through the categories or enter a search query above.")
    
    # Display all FAQs from selected category
    for faq in faq_data.get(category, []):
        st.subheader(faq["question"])
        st.write(faq["answer"])
