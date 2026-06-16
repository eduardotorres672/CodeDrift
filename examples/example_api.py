"""Example API module with documentation"""


def get_user(user_id: int, include_profile: bool = False) -> dict:
    """
    Get user by ID.
    
    Args:
        user_id (int): The user identifier
        include_profile (bool): Whether to include profile data
        
    Returns:
        dict: User object with name, email, and optionally profile
        
    Example:
        >>> user = get_user(123)
        >>> print(user['name'])
        "John Doe"
    """
    return {
        "id": user_id,
        "name": "John Doe",
        "email": "john@example.com",
        "profile": {} if include_profile else None,
    }


def create_post(title: str, content: str, author_id: int) -> dict:
    """
    Create a new blog post.
    
    Args:
        title (str): Post title
        content (str): Post content
        author_id (int): Author user ID
        
    Returns:
        dict: Created post with id, timestamp
    """
    return {
        "id": 1,
        "title": title,
        "content": content,
        "author_id": author_id,
        "created_at": "2024-01-01T00:00:00Z",
    }


def update_user_email(user_id: int, new_email: str, verified: bool) -> dict:
    # DRIFT: Missing docstring!
    return {
        "id": user_id,
        "email": new_email,
        "verified": verified,
    }


def delete_post(post_id: int, force: bool = False) -> bool:
    """
    Delete a blog post.
    
    Args:
        post_id (int): Post ID
        # DRIFT: Missing 'force' parameter in docstring!
        
    Returns:
        bool: True if deleted successfully
    """
    return True
