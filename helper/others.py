
#This page contains the miscellaneous helper functions that are used in the bot  


def message_type(messgae):
    if messgae.document:
        return 'document'
    elif messgae.video:
        return 'video'
    elif messgae.audio:
        return 'audio'
    elif messgae.photo:
        return 'photo'
    else:
        return None
    

def get_file_name(message):
    if message.document:
        return message.document.file_name
    elif message.video:
        return message.video.file_name if message.video.file_name else message.video.file_id
    elif message.audio:
        return message.audio.file_name if message.audio.file_name else message.audio.file_id
    elif message.photo:
        return message.photo.file_name if message.photo.file_name else message.photo.file_id
    else:
        return None
    
def get_file_size(message):
    if message.document:
        return message.document.file_size
    elif message.video:
        return message.video.file_size
    elif message.audio:
        return message.audio.file_size
    elif message.photo:
        return message.photo.file_size