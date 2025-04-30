from langchain.prompts import ChatPromptTemplate

extract_basic = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant to extract basic invoice information."),
    ("user", "다음 텍스트에서 송장번호(invoice_number), 수출자(exporter), 금액(amount)을 JSON 형식으로 반환하세요.\n\n{text}")
])