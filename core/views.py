from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile,Post,LikePost, Comment, Subcomment,User


def index(request):
    return render(request, 'landingpage.html')


def signup(request):
    if request.method == 'POST':
        username= request.POST['Username']
        email= request.POST['Email']
        password= request.POST['Password']
        confpassword= request.POST['Password2']

        if password == confpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken.')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken.')
                return redirect('signup')
            else:
                user= User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login= auth.authenticate(username=username, password=password)
                auth.login(request,user_login)

                user_model= User.objects.get(username=username)
                new_profile = Profile.objects.create(user= user_model, id_user= user_model.id)
                new_profile.save()
                return redirect('profilepage')
        else:
            messages.info(request, 'Password not matching.')
            return redirect('signup')


    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username= request.POST['Username']
        password= request.POST['Password']
        user= auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('upload')
        else:
            messages.info(request, 'Invalid Credentials.')
            return redirect('signin')
    else:
        return render(request, 'signin.html' )

@login_required(login_url='signin')   
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')  
def profilepage(request):
    user_profile= Profile.objects.get(user= request.user)
    if request.method == 'POST':
        if request.FILES.get('profile-image')== None:
            image= user_profile.profileimg
            bio= request.POST['bio']
            location= request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('profile-image') != None:
            image = request.FILES.get('profile-image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('profilepage')
    else:
        return render(request, 'profilepage.html', {'user_profile': user_profile})
    

def upload(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts = Post.objects.all()
    context = {
        'user_profile': user_profile,
        'posts': posts,  
    }
    if request.method == 'POST':
        if request.FILES.get('post-image')== None:
            # img=Post._meta.get_field('post_image').get_default()
            new_post = Post(
        user=user_profile,
        title=request.POST.get('post-title'),
        community=request.POST.get('post-community'),  
        caption=request.POST.get('post-caption'),
    )
            new_post.save()

        if request.FILES.get('post-image') != None:
            new_post = Post(
            user=user_profile,
            post_image=request.FILES.get('post-image'),
            title=request.POST.get('post-title'),
            community=request.POST.get('post-community'),  
            caption=request.POST.get('post-caption'),
        )
            new_post.save()
        
        return redirect('upload')
    else:
        return render(request, 'homepage.html',context)

def like_post(request):
    username= request.user.username
    post_id= request.GET.get('post_id')
    post= Post.objects.get(id=post_id)

    like_filter= LikePost.objects.filter(post_id=post_id,username=username).first()

    if like_filter== None:
        new_like= LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes=post.no_of_likes+1
        post.save()
        return redirect('upload')
    else:
        like_filter.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('upload')

from django.shortcuts import render
from .models import Post, Profile

def search(request):
    if request.method == 'POST':
        user_search = request.POST['s1']
        get_user = User.objects.filter(username = user_search)
        print(get_user)
        print("hehehe",user_search)
        # Query Posts with the 'user' field from the Post model
        posts_by_user = Post.objects.filter(user=user_search)
        print(posts_by_user, "RANDIKHANA")
        # Query Profiles with the 'user' field from the Profile model
        profile_user = Profile.objects.filter(user=get_user[0])
        print(profile_user,"SURABHI")
        context1 = {
            'postings': posts_by_user,
            'prof' : profile_user
        }
        print(context1)
        
        return render(request, 'search.html', context1)


def post_detail(request,post_id):
    #post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post)
    
    if request.method == 'POST':
        if 'comment' in request.POST:
            comment_text = request.POST['comment_text']  
            if comment_text:
                comment = Comment(text=comment_text, post=post)
                comment.save()
                return redirect('post_detail', post_id=post_id)
        elif 'subcomment' in request.POST:
            subcomment_text = request.POST['subcomment_text'] 
            comment_id = request.POST['comment_id']
            if subcomment_text and comment_id:
                comment = Comment.objects.get(pk=comment_id)
                subcomment = Subcomment(text=subcomment_text, comment=comment)
                subcomment.save()
                return redirect('post_detail', post_id=post_id)

    return render(request, 'comments.html', {
        'post': post,
        'comments': comments,
    })