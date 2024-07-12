function openEditModal(commentId, commentContent) {
    const editCommentModal = new bootstrap.Modal(document.getElementById('editCommentModal'));
    document.getElementById('editCommentContent').value = commentContent;
    document.getElementById('editCommentForm').action = `/interactions/comments/section/edit/${commentId}/`;
    editCommentModal.show();
}

function openDeleteModal(commentId) {
    const deleteCommentModal = new bootstrap.Modal(document.getElementById('deleteCommentModal'));
    document.getElementById('deleteCommentForm').action = `/interactions/comments/section/delete/${commentId}/`;
    deleteCommentModal.show();
}
