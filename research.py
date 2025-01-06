#%%
# Warning control
import warnings
warnings.filterwarnings('ignore')
import streamlit as st
import clipboard

#%%
from crewai import Crew, Agent, Task, LLM
#%%
# api_key='AIzaSyDL0wFZNtM82Y0mSyj6rq9hGdPPcCMyfVI'
api_key = st.secrets["API_KEY"]
#%%
llm = LLM(model="gemini/gemini-1.5-pro", temperature=0.9, verbose=True, api_key=api_key)
#%%
planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article "
              "about the topic: {topic}."
              "You collect information that helps the "
              "audience learn something "
              "and make informed decisions. "
              "Your work is the basis for "
              "the Content Writer to write an article on this topic.",
    allow_delegation=False,
	verbose=True,
    llm=llm,
)
#%%
writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate "
         "opinion piece about the topic: {topic}",
    backstory="You're working on a writing "
              "a new opinion piece about the topic: {topic}. "
              "You base your writing on the work of "
              "the Content Planner, who provides an outline "
              "and relevant context about the topic. "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provide by the Content Planner. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provide by the Content Planner. "
              "You acknowledge in your opinion piece "
              "when your statements are opinions "
              "as opposed to objective statements.",
    allow_delegation=False,
    verbose=True,
    llm=llm,
)
#%%
editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with "
         "the writing style of the organization. ",
    backstory="You are an editor who receives a blog post "
              "from the Content Writer. "
              "Your goal is to review the blog post "
              "to ensure that it follows journalistic best practices,"
              "provides balanced viewpoints "
              "when providing opinions or assertions, "
              "and also avoids major controversial topics "
              "or opinions when possible.",
    allow_delegation=False,
    verbose=True,
    llm=llm,
)
#%%
plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
            "their interests and pain points.\n"
        "3. Develop a detailed content outline including "
            "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
    agent=planner,
)
#%%
write = Task(
    description=(
        "1. Use the content plan to craft a compelling "
            "blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
		"3. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
        "4. Ensure the post is structured with an "
            "engaging introduction, insightful body, "
            "and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
    ),
    expected_output="A well-written blog post "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs.",
    agent=writer,
)
#%%
edit = Task(
    description=("Proofread the given blog post for "
                 "grammatical errors and "
                 "alignment with the brand's voice."),
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication, "
                    "each section should have 2 or 3 paragraphs.",
    agent=editor
)
#%%
crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=True
)
#%%
# result = crew.kickoff(inputs={"topic": "Artificial Intelligence"})
#%%
# from IPython.display import Markdown
# Markdown(result.raw)

def generate_markdown(topic):
  """
  Generates markdown content using Crew AI.
  This is a placeholder function.
  You'll need to replace this with the actual Crew AI integration.
  """
  # Replace with your actual Crew AI logic
  markdown_content = crew.kickoff(inputs={f"topic": f"{topic}"})
  return markdown_content

# Streamlit App
st.title("Research Buddy & Article Writer")


# User input for research topic
topic = st.text_input("Enter the topic to research:")

# Generate and display markdown
if st.button("Search"):
  if topic:
    markdown_content = generate_markdown(topic)
    st.markdown(markdown_content)

    # Copy to clipboard button
    # st.button("Copy to Clipboard", on_click=lambda: clipboard.copy(markdown_content))
  else:
    st.warning("Please enter a topic to research.")