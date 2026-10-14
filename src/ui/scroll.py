def clamp_scroll(
    offset: int,
    content_height: int,
    viewport_height: int
) -> int:
    max_scroll = max(
        0,
        content_height - viewport_height
    )
    
    return max(
        0,
        min(offset, max_scroll)
    )