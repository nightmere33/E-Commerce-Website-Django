from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm
from django.contrib.auth.decorators import login_required
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.paginator import Paginator
from core.models import Category

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
<<<<<<< HEAD
        'categories': Category.objects.all(),
=======
>>>>>>> 73ca047f2a58b743c6006f48a332eb4dc71b8aa2
    } )



@login_required
def detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    messages = conversation.messages.all().order_by('-created_at')
    
    # Pagination - 10 messages per page
    paginator = Paginator(messages, 10)
    page_number = request.GET.get('page')
    messages = paginator.get_page(page_number)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            # Optionally, you can redirect to the same page to avoid resubmission
            return redirect('conversation:detail', pk=pk)
    else: 
        form = ConversationMessageForm()
    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form,
    })

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

def index(request):
    all_items = Item.objects.filter(is_sold=False).order_by('name')
    items = list(all_items)  # Convertir en liste pour pouvoir manipuler l'ordre
    
    return render(request, 'core/index.html', {
        'categories': Category.objects.all(),
        'items': items,
    })