import streamlit as st
import pandas as pd
import ast
# from app import chatbot
import time
import openai
endpoint = 'https://allbirds.openai.azure.com/'
region = 'eastus'
key = 'd67d19908eba4902af4903c270547bba'
openai.api_key = key
openai.api_base = endpoint
openai.api_type = 'azure'
openai.api_version = "2023-03-15-preview"

data=pd.read_csv('flipkart_com-ecommerce_sample.csv')


st.set_page_config(page_title="Home", page_icon=None, layout="centered",
                   initial_sidebar_state="auto", menu_items=None)


## logo
with st.sidebar:
    st.markdown("""<div style='text-align: left; margin-top:-50px;margin-left:-190px;'>
    <img src="https://affine.ai/wp-content/uploads/2023/05/Affine-Logo.svg" alt="logo" width="700" height="80">
    </div>""", unsafe_allow_html=True)


st.markdown("""
    <div style='text-align: center; margin-top:-70px; margin-bottom: 5px;margin-left: -50px;'>
    <h2 style='font-size: 40px; font-family: Courier New, monospace;
                    letter-spacing: 2px; text-decoration: none;'>
    <img src="https://acis.affineanalytics.co.in/assets/images/logo_small.png" alt="logo" width="70" height="60">
    <span style='background: linear-gradient(45deg, #ed4965, #c05aaf);
                            -webkit-background-clip: text;
                            -webkit-text-fill-color: transparent;
                            text-shadow: none;'>
                    Intelli-Shop
    </span>
    <span style='font-size: 40%;'>
    <sup style='position: relative; top: 5px; color: #ed4965;'>by Affine</sup>
    </span>
    </h2>
    </div>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
        st.session_state.messages = []

if "product_data" not in st.session_state:
        st.session_state.product_data = []

# Shopping cart
cart = []


# Sidebar filters
st.sidebar.header("Filters")
max_price = st.sidebar.slider("Max Price", min_value=0.0, max_value=5000.0, value=100.0)

# Filter products based on price
filtered_data = data[data["discounted_price"] <= max_price]

st.sidebar.header("Products")
with st.sidebar:
    # Display filtered products with buttons
    for index, row in filtered_data.iterrows():
            st.write(f"**{row['product_name']}**")
            st.image(ast.literal_eval(row["image"])[0], width=100)
            st.write(row["product_category_tree"])
            st.write(f"Price: ${row['discounted_price']:.2f}")
            if st.button(f"Select",key=index):
                cart.append(row.to_dict())
                



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if not cart:     
    print("Your cart is empty.")
else:  
    # total_price = sum(item["discounted_price"] for item in cart)
    # st.sidebar.write(f"Total Price: ${total_price:.2f}")
    # for i, item in enumerate(cart):
    #     st.sidebar.write(f"**{i + 1}. {item['product_name']}** - ${item['discounted_price']:.2f}")
    st.session_state.messages.append(
            {"role": "assistant", "content": f"Hi!,How can I help with this product {cart[0]['product_name']}"})
    with st.chat_message("assistant"):
        st.markdown(f"Hi!,How can I help with this product {cart[0]['product_name']}")
        keys=[key for key in cart[0] if key not in ['is_FK_Advantage_product','image','pid','product_category_tree','product_url','crawl_timestamp','uniq_id']]
        print(keys)
        # st.markdown(keys)
        product_data=' '.join([f'{i}::'+str(cart[0][i])+';' for i in keys])
        st.session_state.product_data.append(product_data)
        print(product_data)


if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        start=time.time()
        # final_prompt=get_prompt(prompt,DEFAULT_SYSTEM_PROMPT)
        # print(final_prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        prompt = """You are user assistant.Give the answer from context only, if question out of context lets return 'Out of context'. add some good emoji and text to attract the user while answering.Expect only specfic answer and in natural languge.
        Example:
        User:Hello
        Assistant:Hello, how can i assist you
        user:what is product price?
        Assistant:20
        Please use following product data to answer the user question : """+st.session_state.product_data[-1] + """user:"""+prompt
        completion = openai.ChatCompletion.create(
                        # engine="gpt4-8k",
                        engine="chatgpt",
                        temperature=0,
                        messages=[{'role': 'system', 'content': 'Your Job to Provide the Product Details'},
                                    {"role": "user", "content": prompt}])

        output = completion["choices"][0]["message"]['content']
        # full_response="Hello"
        end=time.time()
        total_time=end-start
        # for response in model.generate([final_prompt]):
        #     full_response += response
        #     message_placeholder.markdown(response + "▌")
        message_placeholder.markdown(output)
        print("*"*50)
        print(output)
        print(f"Total Time :: {round(total_time)} sec")
    st.session_state.messages.append(
        {"role": "assistant", "content": output}
    )
        


            





