from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.account.models import EmailAddress
from .models import Comment, Favourite
from .forms import CommentForm
from manual.models import Section, Subsection


# Create your views here.
def comment_list(request):
    comments = Comment.objects.filter(user=request.user)
    return render(request, 'interactions/comment_list.html',
                  {'comments': comments})


def add_comment(request, subsection_id):
    subsection = get_object_or_404(Subsection, id=subsection_id)
    email_verified = EmailAddress.objects.filter(user=request.user,
                                                 verified=True).exists()

    if not email_verified:
        return render(request,
                      'interactions/email_not_verified.html')

    if not request.user.is_approved:
        return render(request, 'interactions/not_approved.html')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.subsection = subsection
            comment.approved = True  # Will change to False if
            # admin approval is needed in the future
            comment.save()
            return redirect('subsection_detail', subsection_id=subsection.id)
    else:
        form = CommentForm()

    return render(request, 'interactions/comment_form.html',
                  {'form': form, 'subsection': subsection})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.approved = True  # Will change to False if
            # admin approval is needed in the future
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Comment updated '
                                                            'successfully')
            return redirect(
                'subsection_detail', subsection_id=comment.subsection.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'interactions/edit_comment.html',
                  {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted '
                                                        'successfully')
        return redirect(
            'subsection_detail', subsection_id=comment.subsection.id)
    return render(request, 'interactions/delete_comment.html',
                  {'comment': comment})


@login_required
def add_favourite(request, content_type, content_id):
    user = request.user
    content_name = ''  # initialise to fix bug UnboundLocalError at
    # /interactions/favourites/add/subsection/1/ cannot access local
    # variable 'content_name' where it is not associated with a value
    if content_type == 'section':
        content = get_object_or_404(Section, id=content_id)
        content_name = content.title
        existing_favourite = Favourite.objects.filter(user=user,
                                                      section=content).first()
    else:
        content = get_object_or_404(Subsection, id=content_id)
        existing_favourite = Favourite.objects.filter(user=user,
                                                      subsection=content).first()

    if existing_favourite:
        existing_favourite.delete()
        messages.success(request, f'Removed "{content_name}" from your '
                                  f'favourites.')
    else:
        if content_type == 'section':
            Favourite.objects.create(user=user, section=content)
        else:
            Favourite.objects.create(user=user, subsection=content)
        messages.success(request, f'Added "{content_name}" to your favourites.')

    return redirect(request.META.get('HTTP_REFERER',
                                     'redirect_if_referer_not_found'))


def add_comment_to_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    email_verified = EmailAddress.objects.filter(user=request.user, verified=True).exists()

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
            comment.approved = True  # Will change to False if admin approval is needed in the future
            comment.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Kommentar abgeschickt. Scrollen Sie nach unten, um Ihre Kommentare zu sehen.')
            return redirect('section_detail_accordion', section_id=section.id)
    else:
        form = CommentForm()

    return render(request, 'interactions/comment_form.html', {'form': form, 'section': section})

@login_required
def edit_section_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user, section__isnull=False)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.approved = True  # Will change to False if admin approval is needed in the future
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Comment updated successfully')
            return redirect('section_detail_accordion', section_id=comment.section.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'interactions/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_section_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user, section__isnull=False)
    if request.method == 'POST':
        section_id = comment.section.id
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted successfully')
        return redirect('section_detail_accordion', section_id=section_id)
    return render(request, 'interactions/delete_comment.html', {'comment': comment})

@login_required
def list_favourites(request):
    user = request.user
    favourite_sections = user.favourites.filter(section__isnull=False)
    favourite_subsections = user.favourites.filter(subsection__isnull=False)
    context = {
        'favourite_sections': favourite_sections,
        'favourite_subsections': favourite_subsections
    }
    return render(request, 'interactions/favourites_list.html', context)


def dashboard(request):
    user = request.user
    favourite_sections = Favourite.objects.filter(user=user,
                                                  section__isnull=False)
    favourite_subsections = Favourite.objects.filter(user=user,
                                                     subsection__isnull=False)
    comments = user.comment_set.all()
    sections = Section.objects.all()


    return render(request, 'interactions/dashboard.html', {
        'user': user,
        'favourite_sections': favourite_sections,
        'favourite_subsections': favourite_subsections,
        'comments': comments,
        'sections': sections,
    })
