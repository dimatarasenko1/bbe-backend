from config import supabase


def get_leaderboard():
    q = (
        supabase.table("Users")
        .select("username", "all_time_answers")
        .gt("all_time_answers", 0)
        .order("all_time_answers", desc=True)
    )
    response = q.execute()
    return response.data
