# Automated Data Extraction 🚀🤖

**Overview**

Automated Data Extraction is a powerful tool designed to streamline the process of retrieving information from various sources. This application empowers users to:

- Upload CSV files or connect directly to Google Sheets.
- Define custom data retrieval prompts using placeholders (e.g., "Get the email address of {company}").
- Execute automated web searches using a language model (LLM) for precise extraction.
- Manage and visualize extracted data within an intuitive dashboard.

## Try it Out! 🚀

The application is accessible at this link: [Automated Data Extraction Streamlit App](https://searchin.streamlit.app/).  **(This link may require an API key)**

This deployed version. However, depending on the configuration, you might need an API key to access the full capabilities.


**Key Features**

1. **User-Friendly Dashboard**
   - **Import Data** 📁: Upload CSV files or seamlessly connect to Google Sheets.
   - **Data Preview** 👀: View a clear overview of data columns to facilitate data selection.
   - **Intuitive Navigation** 🧭: Effortlessly interact with the application for efficient data extraction.

2. **Customizable Query Input**
   - **Prompt Creation** 📝: Define specific prompts for data retrieval using placeholders.
   - **Dynamic Generation** 🔄: Generate queries tailored to each entry in the selected column.

3. **Automated Web Searches**
   - **Search Execution** 🔍: Conduct web searches based on user-defined prompts.
   - **Relevant Retrieval** 🎯: Gather pertinent search results for processing.

4. **Powerful LLM Integration**
   - **Model Utilization** 🤖: Leverage the capabilities of a language model to extract targeted information from search results.
   - **Data Extraction** ⛏️: Extract various data types, including email addresses and other relevant details.

5. **Data Display and Export Options**
   - **Structured Presentation** 📊: View extracted information in a well-organized table format.
   - **Export Flexibility** 💾: Download extracted data as CSV files or directly update connected Google Sheets.

**Advanced Features**

- **Complex Query Templates** 🧠: Construct sophisticated queries that retrieve multiple fields in one prompt (e.g., "Get the email and address for {company}").
- **Google Sheets Integration** 🔗: Effortlessly write extracted data back to Google Sheets, boosting workflow optimization.
- **Error Handling and Notification System** 🚨: Receive real-time notifications of any issues during API calls or LLM queries, enabling swift troubleshooting.

**Setup Instructions**

**Prerequisites**

- Python 3.7 or later
- API Keys for SerpAPI, Groq (or OpenAI), and Google Sheets

**Installation and Running Steps**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Shreyaaaash/WEB-SEARCH-DATA-EXTRACTION.git

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
  use `venv\Scripts\activate` on Windows

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

4. **Configure Environment Variables**
   ```bash
   SERP_API_KEY="your_serp_api_key" GROQ_API_KEY="your_groq_api_key"

5. **Run the App**
   ```bash
   streamlit run app.py

## Advanced Features

- **Complex Query Templates 🧠**: 
  Construct sophisticated queries that retrieve multiple fields in one prompt. For example, you can use a query like:
  > "Get the CEO, headquarters, and revenue for {company}".

- **Google Sheets Integration 🔗**: 
  Effortlessly write extracted data back to Google Sheets, boosting workflow optimization. This integration allows you to:
  - Fetch data from Google Sheets and process it seamlessly.
  - Automatically update your Google Sheets with new data entries based on user-defined triggers.
  - Support both public and private Google Sheets with flexible configuration options.

- **Error Handling and Notification System 🚨**: 
  Receive real-time notifications of any issues during API calls or LLM queries, enabling swift troubleshooting. This system ensures:
  - Immediate alerts for failed data retrieval attempts.
  - Clear error messages that help identify issues quickly.
  - Enhanced reliability and user experience through proactive monitoring.


## License 📄

This project is licensed under the MIT License; refer to the `LICENSE.md` file for more details.

## Contributing 🤝

We welcome contributions! Please feel free to submit issues or pull requests on GitHub.

## Contact 📬

For questions or feedback, please reach out via [shreyash4002@gmail.com].

---

Thank you for using Automated Data Extraction! 🙌

