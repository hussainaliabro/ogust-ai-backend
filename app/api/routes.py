from fastapi import APIRouter, HTTPException

from app.models.request_models import (
    StartDocumentRequest,
    ReplyQuestionsRequest,
    GenerateDocumentRequest,
)

from app.models.response_models import (
    StartDocumentResponse,
    ReplyQuestionsResponse,
    GenerateDocumentResponse,
    GeneratedFiles,
)

from app.services.ai_service import (
    analyze_document_request,
    generate_document,
)

from app.services.session_service import session_service

from app.services.pdf_service import (
    create_pdf,
    save_docx,
    save_html,
)

router = APIRouter(prefix="/document", tags=["Document"])
@router.post(
    "/start",
    response_model=StartDocumentResponse,
)
async def start_document(
    request: StartDocumentRequest,
):

    # AI analyzes request
    result = analyze_document_request(
        request.instruction
    )

    # Create session
    session = session_service.create_session(
        instruction=request.instruction,
        title=result["title"],
        questions=result["questions"],
    )

    return StartDocumentResponse(
        status="success",
        message="Session created successfully.",
        session_id=session.session_id,
        document_title=session.title,
        questions=session.questions,
        ready_to_generate=len(session.questions) == 0,
    )

@router.post(
    "/reply",
    response_model=ReplyQuestionsResponse,
)
async def reply_questions(
    request: ReplyQuestionsRequest,
):

    session = session_service.save_answers(
        request.session_id,
        request.answers,
    )

    answered = len(session.answers)

    remaining = max(
        len(session.questions) - answered,
        0,
    )

    return ReplyQuestionsResponse(
        status="success",
        message="Answers saved successfully.",
        session_id=session.session_id,
        answered_questions=answered,
        remaining_questions=remaining,
        ready_to_generate=True,
    )
@router.post(
    "/generate",
    response_model=GenerateDocumentResponse,
)
async def generate_document_route(
    request: GenerateDocumentRequest,
):

    session = session_service.get_session(
        request.session_id
    )

    if session.generated:
        raise HTTPException(
            status_code=400,
            detail="This session has already generated a document."
        )

    html = generate_document(session)

    html_path = save_html(
        session.title,
        html,
    )

    pdf_path = await create_pdf(
        session.title,
        html,
    )

    docx_path = save_docx(
        session.title,
        html,
    )

    session_service.mark_generated(
        session.session_id
    )

    return GenerateDocumentResponse(
        status="success",
        message="Document generated successfully.",
        session_id=session.session_id,
        document_title=session.title,
        files=GeneratedFiles(
            html=html_path,
            pdf=pdf_path,
            docx=docx_path,
        ),
    )