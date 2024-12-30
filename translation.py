class Translation(object):
    START = "<b>👋 Hi {name}!</b> \n<code>I'm a simple bot to help you transfer files between Telegram and your DMS account for data-free downloads.</code> \n<b>Just forward a file here to get started. 🚀</b>"
    DOWNLOADING = "📥 Downloading your file to the server..."
    DOWNLOADED = "🎉 File downloaded successfully! Now uploading to DMS..."
    DOWNLOAD_ERROR = "❌ Oops! Something went wrong while downloading the file."
    UPLOADING = "📤 Uploading your file to DMS..."
    UPLOADED = "🎉 File uploaded successfully to your DMS account!"
    HELP = "💡 Simply forward a file to me, and I'll handle the rest!"
    ABOUT = "<b>About This Bot:</b> \n✨ Created by Kajatheepan. \n\ud83d\udd17 Source Code: <a href='link'>GitHub</a>"
    PROGRESS = "<b>⏳ Downloading your file:\nProgress: {prog}%\nTotal Size: {total}\nDownloaded: {current} 📍</b>"
    BATCH = "🔧 Send all the files you want to upload in a single batch. \n<b>When done, send <code>/done</code> or click the 'Done' button.</b>"
    LOGIN = "🔐 Please log in to your DMS account to upload files."
    BATCH_ADD = "📦 Continue forwarding your files. \n<b>When done, send <code>/done</code> or click the 'Done' button.</b>"
    BATCH_DONE = "🎉 All files uploaded successfully!"
    BATCH_CLOSE = "❌ Batch upload has been cancelled."
    BATCH_EMPTY = "📦 No files to upload. Please send files first!"
    BATCH_DONE= "🎉{n} files uploaded successfully! \n\n <b>Links: {urls} <b>"
    DOWNLOAD = "🔍 File found and ready to download!"
    UPLOAD_ERROR = "❌ Oops! Something went wrong while uploading the file."
    LOGIN_CALL = "<b>🔐 Please enter your DMS login credentials in this format:</b> \n<code>USERNAME PASSWORD</code>"
    LOGIN_ERROR = "⚠ Incorrect login details. Please try again: \n<code>USERNAME PASSWORD</code>"
    LOGIN_FAILED = "❌ Login failed. Please check your credentials and try again."
    LOGIN_SUCCESS = "🎉 Login successful! You can now upload files."
    LOGIN_FINISH = "🏠 You are now logged in to your DMS account."
    LOGIN_FIRST = "🔐 Please log in before uploading your files."
    QUOTA_EXCEEDED = "⚠ DMS free quota limit reached. \nPlease delete some files and try again!"
    SHARE_FILE='🔗 File Downloaded successfully! \n \n <b>Link: {link} <b>'

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class InlineKeyboard(object):
    START = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('💡 Help', callback_data='help'),
                InlineKeyboardButton('✨ About', callback_data='about'),
            ],
            [
                InlineKeyboardButton('📦 Batch Upload', callback_data='batch'),
                InlineKeyboardButton('🔐 DMS Login', callback_data='login')
            ]
        ]
    )

    HELP = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('✨ About', callback_data='about')
            ]
        ]
    )

    ABOUT = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('◀ Back', callback_data='start')
            ]
        ]
    )

    LOGIN = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('🔐 Login', callback_data='dmslogin')
            ]
        ]
    )

    BATCH_ADD = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('✅ Done', callback_data='done'),
                InlineKeyboardButton('❌ Close', callback_data='close'),
            ],
        ]
    )

    DOWNLOAD = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('🔍 Download', callback_data='download'),
            InlineKeyboardButton('❌ Cancel', callback_data='cancel')
        ]
    ])

    LOGIN_FINISH = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('🏠 Home', callback_data='start'),
                InlineKeyboardButton('❌ Close', callback_data='close')
            ]
        ]
    )
    BATCH_CANCEL=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('❌ cancel',callback_data='cancel_batch')
            ]
        ]
    )