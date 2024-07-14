from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.account.models import EmailAddress
from .models import Comment, Favourite
from .forms import CommentForm
from manual.models import Section, Subsection


# Create your views here.
def comment_list(request):
    """
    High-level description:
    This view displays a list of comments made by the user.

    model: `Comment`

    **Context:** - `comments`: A queryset of comments made by the
    authenticated user, retrieved from the `Comment` model.

    Template:
    This view returns the `interactions/comment_list.html` template.
    """
    comments = Comment.objects.filter(user=request.user)
    return render(request, 'interactions/comment_list.html',
                  {'comments': comments})


@login_required
def add_favourite(request, content_type, content_id):
    """
    High-level description: This view allows the user to add or remove a
    favourite section or subsection.

    model: `Favourite`

    **Context:** This view does not return any context variables. It
    redirects to the referer page.

    Template:
    This view does not render a template directly.
    """
    user = request.user
    if content_type == 'section':
        content = get_object_or_404(Section, id=content_id)
        existing_favourite = Favourite.objects.filter(user=user,
                                                      section=content).first()
    else:
        content = get_object_or_404(Subsection, id=content_id)
        existing_favourite = Favourite.objects.filter(
            user=user, subsection=content).first()

    if existing_favourite:
        existing_favourite.delete()
        messages.success(request, f'Entfernt "{content}" aus Ihren '
                                  f'Favoriten.')
    else:
        if content_type == 'section':
            Favourite.objects.create(user=user, section=content)
        else:
            Favourite.objects.create(user=user, subsection=content)
        messages.success(request, f'"{content}" zu Ihren Favoriten '
                                  f'hinzugefügt.')

    return redirect(request.META.get('HTTP_REFERER',
                                     'redirect_if_referer_not_found'))


def add_comment_to_section(request, section_id):
    """
    High-level description:
    This view allows the user to add a comment to a specific section.

    model: `Comment`
    form: `CommentForm`

    **Context:** - `form`: The form to submit a new comment, using the
    `CommentForm`. - `section`: The specific section being commented on,
    retrieved from the `Section` model.

    Template:
    This view returns the `interactions/comment_form.html` template.
    """
    section = get_object_or_404(Section, id=section_id)
    email_verified = EmailAddress.objects.filter(user=request.user,
                                                 verified=True).exists()

    if not email_verified:
        return render(request, 'interactions/email_not_verified.html')

    if not request.user.is_approved:
        return render(request, 'interactions/not_approved.html')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.section = section
            comment.approved = True
            # Will change to False if admin approval is needed in the future
            comment.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Kommentar abgeschickt. Scrollen Sie nach '
                                 'unten, um Ihre Kommentare zu sehen.')
            return redirect('section_detail_accordion', section_id=section.id)
    else:
        form = CommentForm()

    return render(request, 'interactions/comment_form.html',
                  {'form': form, 'section': section})


@login_required
def edit_section_comment(request, comment_id):
    """
    High-level description:
    This view allows the user to edit their comment on a specific section.

    model: `Comment`
    form: `CommentForm`

    **Context:** - `form`: The form to edit an existing comment, using the
    `CommentForm`. - `comment`: The specific comment being edited, retrieved
    from the `Comment` model.

    Template:
    This view returns the `interactions/edit_comment.html` template.
    """
    comment = get_object_or_404(Comment, id=comment_id, user=request.user,
                                section__isnull=False)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.approved = True
            # Will change to False if admin approval is needed in the future
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Kommentar erfolgreich aktualisiert")
            return redirect('section_detail_accordion',
                            section_id=comment.section.id)
    else:
        form = CommentForm(instance=comment)
    return render(request,
                  'interactions/edit_comment.html',
                  {'form': form, 'comment': comment})


@login_required
def delete_section_comment(request, comment_id):
    """
    High-level description:
    This view allows the user to delete their comment on a specific section.

    model: `Comment`

    **Context:** - `comment`: The specific comment being deleted, retrieved
    from the `Comment` model.

    Template:
    This view returns the `interactions/delete_comment.html` template.
    """
    comment = get_object_or_404(Comment, id=comment_id,
                                user=request.user, section__isnull=False)
    if request.method == 'POST':
        section_id = comment.section.id
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Kommentar '
                                                        'erfolgreich gelöscht')
        return redirect('section_detail_accordion', section_id=section_id)
    return render(request, 'interactions/delete_comment.html',
                  {'comment': comment})


@login_required
def list_favourites(request):
    """
    High-level description:
    This view displays a list of the user's favourite sections and subsections.

    model: `Favourite`

    **Context:** - `favourite_sections`: A queryset of the user's favourite
    sections, retrieved from the `Favourite` model. -
    `favourite_subsections`: A queryset of the user's favourite subsections,
    retrieved from the `Favourite` model.

    Template:
    This view returns the `interactions/favourites_list.html` template.
    """
    user = request.user
    favourite_sections = user.favourites.filter(section__isnull=False)
    favourite_subsections = user.favourites.filter(subsection__isnull=False)
    context = {
        'favourite_sections': favourite_sections,
        'favourite_subsections': favourite_subsections
    }
    return render(request,
                  'interactions/favourites_list.html', context)


def dashboard(request):
    """
    High-level description: This view displays the user's dashboard with
    their favourite sections, subsections, and comments.

    model: `Favourite`, `Comment`, `Section`

    **Context:** - `user`: The authenticated user. - `favourite_sections`: A
    queryset of the user's favourite sections, retrieved from the
    `Favourite` model. - `favourite_subsections`: A queryset of the user's
    favourite subsections, retrieved from the `Favourite` model. -
    `comments`: A queryset of the user's comments, retrieved from the
    `Comment` model. - `sections`: A queryset of all sections, retrieved
    from the `Section` model.

    Template:
    This view returns the `interactions/dashboard.html` template.
    """
    user = request.user
    favourite_sections = Favourite.objects.filter(
        user=user, section__isnull=False).order_by('section__title')
    favourite_subsections = Favourite.objects.filter(
        user=user, subsection__isnull=False).order_by(
        'subsection__title')
    comments = user.comment_set.all()
    sections = Section.objects.all().order_by('title')

    return render(request, 'interactions/dashboard.html', {
        'user': user,
        'favourite_sections': favourite_sections,
        'favourite_subsections': favourite_subsections,
        'comments': comments,
        'sections': sections,
    })
