from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.hashers import make_password,check_password
from .models import Account,Post,Like
from django.http import JsonResponse
from django.db import IntegrityError
# Create your views here.

def sing_up_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        photo = request.FILES.get('photo')

        try:
            Account.objects.create(
                name=name,
                email=email,
                password=make_password(password),
                photo=photo
            )
            return redirect('login')
        except IntegrityError:
            return render(request, 'sing.html', {'error': 'This email is already registered!'})

    return render(request, 'sing.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')   # email নিলাম
        raw_password = request.POST.get('password')

        try:
            user = Account.objects.get(email=email)  
        except Account.DoesNotExist:
            return render(request, 'log.html', {'error': 'Email not found'})

        if check_password(raw_password, user.password):
            request.session['user_id'] = user.id
            return redirect('explore')
        else:
            return render(request, 'log.html', {'error': 'Password wrong'})

    return render(request, 'log.html')







def profile_page(request, user_id):
    logged_id = request.session.get('user_id')
    if not logged_id:
        return redirect('login')  # login লাগবে

    if int(logged_id) != int(user_id):
        # চাইলে 403 বা অন্য পেজ দেখাতে পারো
        return render(request, 'forbidden.html', status=403)

    user = get_object_or_404(Account, id=user_id)
    posts = Post.objects.filter(user=user).order_by("-created_at")  # user-এর সব পোস্ট
    return render(request, 'profile.html', {'user': user,'posts':posts})






def logout_view(request):
    request.session.flush()
    return redirect('login')



def reset(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        new_pass=request.POST.get('newpass')
        
        
        try:
            user=Account.objects.get(email=email)
            user.password=make_password(new_pass)
            user.save()
            return redirect('reset_done')
        except Account.DoesNotExist:
            return render(request,'reset.html',{'msg':'Email not found'})
        
        
        
    return render(request,'reset.html')
            
            
            
            
            
def reset_done(request):
    return render(request,'reset_done.html')









def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    user_id = request.session.get("user_id")  # logged in user id
    return render(request, "explore.html", {"posts": posts, "user_id": user_id})





def create_post(request, user_id):
    user = get_object_or_404(Account, id=user_id)

    if request.method == "POST":
        heading = request.POST.get("heading")
        content = request.POST.get("content")

        Post.objects.create(user=user, heading=heading, content=content)
        return redirect("profile", user_id=user.id)

    return render(request, "create_post.html", {"user": user})


def like_post(request, post_id):
    logged_id = request.session.get('user_id')
    if not logged_id:
        return JsonResponse({'error': 'login required'}, status=403)

    post = get_object_or_404(Post, id=post_id)
    user = get_object_or_404(Account, id=logged_id)

    like, created = Like.objects.get_or_create(user=user, post=post)
    if not created:  # already liked → unlike
        like.delete()
        liked = False
    else:
        liked = True

    # নতুন like count হিসাব
    count = Like.objects.filter(post=post).count()

    return JsonResponse({'liked': liked, 'like_count': count})

    
    
def update_post(request, post_id):
    logged_id = request.session.get('user_id')
    if not logged_id:
        return redirect('login')

    post = get_object_or_404(Post, id=post_id)

    # কেবল owner ই edit করতে পারবে
    if post.user.id != logged_id:
        return render(request, 'forbidden.html', status=403)

    if request.method == "POST":
        heading = request.POST.get("heading")
        content = request.POST.get("content")

        post.heading = heading
        post.content = content
        post.save()

        return redirect("profile", user_id=post.user.id)

    return render(request, "update.html", {"post": post})
            
            
            
            
            
            
            
            
            
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "post_detail.html", {"post": post})





def use_pro(request,user_id):
    user = get_object_or_404(Account, id=user_id)
    posts = Post.objects.filter(user=user).order_by("-created_at")

    return render(request, 'user_profile.html', {
        'profile_user': user,   # profile_owner
        'posts': posts
    })
     
