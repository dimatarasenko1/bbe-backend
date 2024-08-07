from config import supabase
from typing import Optional, List, Dict
from models.quiz import QuizDetails


def validate_quizzes(quizzes: List[Dict]) -> List[QuizDetails]:
    d = []
    for quiz in quizzes:
        q_d = quiz
        if quiz.get("Users"):
            q_d["username"] = quiz["Users"]["username"]
        del q_d["Users"]
        d.append(QuizDetails(**q_d))
    return d


def get_quizzes(
    page: int,
    query: Optional[str] = None,
    category: Optional[str] = None,
    seen: Optional[List[str]] = [],
) -> Dict[str, QuizDetails]:
    per_page = 20
    offset = (page - 1) * per_page

    # Create the base query for counting total matching records
    count_query = supabase.table("Quizzes").select("id", count="exact")

    # Apply filters if they exist
    if query:
        count_query = count_query.ilike("title", f"%{query}%")
    if category:
        count_query = count_query.eq("category", category)
    if seen:
        seen = seen[0].split(",")
        print(seen)
        count_query = count_query.not_.in_("id", seen)

    # Execute the count query
    count_response = count_query.execute()
    if not count_response.count:
        if count_response.count == 0:
            return {
                "page": page,
                "per_page": per_page,
                "total_pages": 0,
                "total_count": 0,
                "data": [],
            }
        else:
            raise Exception(f"Failed to fetch quiz count: {count_response}")

    total_count = count_response.count
    total_pages = (total_count + per_page - 1) // per_page

    # Create the base query for fetching the paginated data
    data_query = (
        supabase.table("Quizzes")
        .select("*", "Users(username)")
        .order("play_count", desc=True)
        .range(offset, offset + per_page - 1)
    )

    # Apply filters if they exist
    if query:
        data_query = data_query.ilike("title", f"%{query}%")
    if category:
        data_query = data_query.eq("category", category)
    if len(seen) > 0:
        data_query = data_query.not_.in_("id", seen)

    # Execute the data query
    data_response = data_query.execute()
    if not data_response.data:
        raise Exception(f"Failed to fetch quizzes: {data_response}")

    quizzes = validate_quizzes(data_response.data)

    return {
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "total_count": total_count,
        "data": quizzes,
    }
