import time

from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    fact_checker_chain,
    critic_chain
)

DEBUG = False


def debug_print(*args):
    if DEBUG:
        print(*args)


def run_research_pipeline(topic: str, update_progress=None) -> dict:

    start_time = time.time()

    state = {

        "status": "Running",

        "search_messages": [],
        "reader_messages": [],

        "search_results": "",
        "scraped_content": "",

        "report": "",
        "fact_check": "",
        "feedback": "",

        "execution_time": 0,

        "search_time": 0,
        "reader_time": 0,
        "writer_time": 0,
        "fact_check_time": 0,
        "critic_time": 0
    }

    # ==================================================
    # STEP 1 : SEARCH
    # ==================================================

    try:

        if update_progress:
            update_progress(0.1, "🔎 Searching the web...")

        t1 = time.time()

        search_agent = build_search_agent()

        search_result = search_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"""
Find recent and reliable information about:

{topic}

Return:
- Important subtopics
- Relevant URLs
- Key findings
"""
                    )
                ]
            }
        )

        state["search_messages"] = search_result["messages"]
        state["search_results"] = search_result["messages"][-1].content

        state["search_time"] = round(
            time.time() - t1,
            2
        )

        debug_print(state["search_results"])

    except Exception as e:

        state["search_results"] = (
            f"Search Agent Error: {str(e)}"
        )

        return state

    # ==================================================
    # STEP 2 : READER
    # ==================================================

    try:

        if update_progress:
            update_progress(0.3, "📖 Reading sources...")

        t2 = time.time()

        reader_agent = build_reader_agent()

        reader_result = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"""
Topic:

{topic}

From the search results below:

1. Identify the most reliable URL.
2. Use web_scrape to extract detailed content.
3. Summarize the page.
4. Include the URL used.
5. Mention important findings.

Search Results:

{state['search_results']}
"""
                    )
                ]
            }
        )

        state["reader_messages"] = reader_result["messages"]
        state["scraped_content"] = (
            reader_result["messages"][-1].content
        )

        state["reader_time"] = round(
            time.time() - t2,
            2
        )

        debug_print(state["scraped_content"])

    except Exception as e:

        state["scraped_content"] = (
            f"Reader Agent Error: {str(e)}"
        )

        return state

    # ==================================================
    # STEP 3 : WRITER
    # ==================================================

    try:

        if update_progress:
            update_progress(0.55, "✍️ Writing report...")

        t3 = time.time()

        research_combined = f"""

Search Results:

{state['search_results']}

Detailed Scraped Content:

{state['scraped_content']}
"""

        state["report"] = writer_chain.invoke(
            {
                "topic": topic,
                "research": research_combined
            }
        )

        state["writer_time"] = round(
            time.time() - t3,
            2
        )

    except Exception as e:

        state["report"] = (
            f"Writer Error: {str(e)}"
        )

        return state

    # ==================================================
    # STEP 4 : FACT CHECKER
    # ==================================================

    try:

        if update_progress:
            update_progress(0.75, "✅ Fact checking...")

        t4 = time.time()

        state["fact_check"] = fact_checker_chain.invoke(
            {
                "report": state["report"]
            }
        )

        state["fact_check_time"] = round(
            time.time() - t4,
            2
        )

    except Exception as e:

        state["fact_check"] = (
            f"Fact Checker Error: {str(e)}"
        )

        return state

    # ==================================================
    # STEP 5 : CRITIC
    # ==================================================

    try:

        if update_progress:
            update_progress(0.9, "⭐ Reviewing report...")

        t5 = time.time()

        state["feedback"] = critic_chain.invoke(
            {
                "report": state["report"],
                "fact_check": state["fact_check"]
            }
        )

        state["critic_time"] = round(
            time.time() - t5,
            2
        )

    except Exception as e:

        state["feedback"] = (
            f"Critic Error: {str(e)}"
        )

        return state

    # ==================================================
    # COMPLETED
    # ==================================================

    state["execution_time"] = round(
        time.time() - start_time,
        2
    )

    state["status"] = "Completed"

    if update_progress:
        update_progress(
            1.0,
            "🎉 Completed"
        )

    return state


if __name__ == "__main__":

    DEBUG = True

    topic = input("\nEnter a research topic: ")

    state = run_research_pipeline(topic)

    print("\nREPORT\n")
    print(state["report"])

    print("\nFACT CHECK\n")
    print(state["fact_check"])

    print("\nCRITIC FEEDBACK\n")
    print(state["feedback"])

    print(
        f"\nExecution Time: {state['execution_time']} sec"
    )