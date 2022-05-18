from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import Http404

from .models import Blog, Comment, Feedback
from .forms import FeedbackForm, CommentForm

# Create your views here.

def handleFeedback(request):
    # create a variable to keep track of the form
    messageSent = False

    if request.method == 'POST':

        form = FeedbackForm(request.POST)
        
         # check if data from the form is clean
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            fromEmail = data['fromEmail']
            message = data['message']
            subject = data['subject']

            fb = Feedback(id=Feedback.objects.count() + 1, name=name, email=fromEmail, subject=subject, message=message)
            fb.save()

            # send the email to the recipent
            send_mail('Feedback', 'Cảm ơn bạn đã gửi phản hồi cho chúng tôi!', 'anonymoustpt11@gmail.com', [fromEmail])

            # set the variable initially created to True
            messageSent = True
    else:
        form = FeedbackForm()

    return render(request, 'users/templates/menu/contact.html', {
        'form': form,
        'messageSent': messageSent,
    })


def BlogDetailView(request, _id):
    try:
        data = Blog.objects.get(id=_id)
        comments = Comment.objects.filter(blog=data)
    except Blog.DoesNotExist:
        raise Http404('Data does not exist')
     
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                user=request.user,
                commentText=form.cleaned_data['commentText'],
                blog=data)
            comment.save()
            return redirect(f'/menu/{_id}#Comment')
    else:
        form = CommentForm()
 
    context = {
            'data': data,
            'form': form,
            'comments': comments,
        }
    return render(request, 'users/templates/menu/detailview.html', context)

def deleteComment(request, id):
    cmt = Comment.objects.get(pk = id)
    blogID = cmt.blog.id
    cmt.delete()
    return redirect(f'/menu/{blogID}#Comment')

def menu_view(request):
    return render(request, 'food_diet/templates/menu.html')
#Begin loss gain
def loss_gain_view(request):
    return render(request, 'food_diet/templates/main/loss_gain/loss_gain.html')
def loss_gain_paper_1_view(request):
    return render(request, 'food_diet/templates/main/loss_gain/LG(1).html')
def loss_gain_paper_2_view(request):
    return render(request, 'food_diet/templates/main/loss_gain/LG(2).html')
def loss_gain_paper_3_view(request):
    return render(request, 'food_diet/templates/main/loss_gain/LG(3).html')
def loss_gain_paper_4_view(request):
    return render(request, 'food_diet/templates/main/loss_gain/LG(4).html')
def loss_gain_paper_5_view(request):
    return render(request, 'food_diet/templates/main/loss_gain/LG(5).html')
def loss_gain_paper_6_view(request):
    return render(request, 'food_diet/templates/main/loss_gain/LG(6).html')

#begin vegan
def vegan_view(request):
    return render(request, 'food_diet/templates/main/vegan/vegan.html')
def vegan_paper_1_view(request):
    return render(request, 'food_diet/templates/main/vegan/vegan(1).html')
def vegan_paper_2_view(request):
    return render(request, 'food_diet/templates/main/vegan/vegan(2).html')
def vegan_paper_3_view(request):
    return render(request, 'food_diet/templates/main/vegan/vegan(3).html')

#Begin other
def other_view(request):
    return render(request, 'food_diet/templates/main/other/other.html')
def other_paper_1_view(request):
    return render(request, 'food_diet/templates/main/other/other(1).html')
def other_paper_2_view(request):
    return render(request, 'food_diet/templates/main/other/other(2).html')
def other_paper_3_view(request):
    return render(request, 'food_diet/templates/main/other/other(3).html')
def other_paper_4_view(request):
    return render(request, 'food_diet/templates/main/other/other(4).html')
def other_paper_5_view(request):
    return render(request, 'food_diet/templates/main/other/other(5).html')
def other_paper_6_view(request):
    return render(request, 'food_diet/templates/main/other/other(6).html')
def other_paper_7_view(request):
    return render(request, 'food_diet/templates/main/other/other(7).html')


#weight gain
def weight_gain(request):
    return render(request, 'food_diet/templates/main/weight gain/weight_gain.html')
def weight_gain_paper(request):
    return render(request, 'food_diet/templates/main/weight gain/weight_gain_paper.html')
def weight_gain_paper_1(request):
    return render(request, 'food_diet/templates/main/weight gain/weight_gain_paper(1).html')
def weight_gain_paper_2(request):
    return render(request, 'food_diet/templates/main/weight gain/weight_gain_paper(2).html')
