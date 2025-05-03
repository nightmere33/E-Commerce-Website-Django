from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm
from django.contrib.auth.decorators import login_required

@login_required
def new_conversation(request,item_pk):
    item = get_object_or_404(Item ,pk = item_pk) # Get the item object or return 404 if not found

    if item.created_by == request.user:
        return redirect('dashboard:index')

    conversations = Conversation.objects.filter(item = item).filter(members__in = [request.user.id]) # Get the conversations for the item

    if conversations :
        pass # redirect to the conversation page if it exists
    
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST) # Create a form instance with the POST data
        if form.is_valid():
            conversation = Conversation.objects.create(item = item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by) # Add the members to the conversation
            conversation.save() # Save the conversation object
            conversation_message = form.save(commit=False) # Create a message object but don't save it yet
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail' , pk= item_pk) # Redirect to the item detail page after saving the message
    else:
        form = ConversationMessageForm()

    return   render(request, 'conversation/new.html',{
        'form': form,
    } )     

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in = [request.user.id]) # Get the conversations for the item

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
    } )

@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in = [request.user.id]).get(pk=pk) # Get the conversation object or return 404 if not found

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
    } )