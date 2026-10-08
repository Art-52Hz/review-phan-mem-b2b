"""Conservative checks for unreviewed model output, not factual verification."""
import re


class DraftReviewRequired(ValueError):
    pass


def validate_generated_draft(content):
    """Reject unsupported evidence signals before the legacy writer saves a file.

    The generator receives no test records. Numeric product ratings and narrated
    first-person experiments therefore require a separate human-reviewed route.
    Passing this check does not establish that any other statement is accurate.
    """
    if not isinstance(content, str) or not content.strip():
        raise DraftReviewRequired('Empty generated draft')
    patterns = {
        'numeric rating': r'\b\d+(?:\.\d+)?\s*(?:/\s*5|out\s+of\s+5|stars?\b)',
        'rating metadata': r'["\']?(?:rating|ratingValue)["\']?\s*:\s*["\']?\d',
        'first-person experiment': (
            r'\b(?:I|we)\s+(?:(?:have|personally|actually|extensively)\s+)*'
            r'(?:tested|benchmarked|used|tried|measured)\b'),
    }
    for label, pattern in patterns.items():
        if re.search(pattern, content, re.IGNORECASE):
            raise DraftReviewRequired('Generated draft requires evidence review: ' + label)
    return content
