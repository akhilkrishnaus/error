
import logging
from struct import pack
import re
import base64
from pyrogram.file_id import FileId
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow.exceptions import ValidationError
from info import DATABASE_URI, DATABASE_NAME, COLLECTION_NAME, USE_CAPTION_FILTER, MAX_B_TN, SECONDDB_URI
from utils import get_settings, save_group_settings
from sample_info import tempDict 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#some basic variables needed
saveMedia = None

#primary db
client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
instance = Instance.from_db(db)

@instance.register
class Media(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

#secondary db
client2 = AsyncIOMotorClient(SECONDDB_URI)
db2 = client2[DATABASE_NAME]
instance2 = Instance.from_db(db2)

@instance2.register
class Media2(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

#3rd

client3 = AsyncIOMotorClient(DATABASE_URI3)
db3 = client[DATABASE_NAME]
instance3 = Instance.from_db(db3)

@instance3.register
class Media3(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

#4th
client4 = AsyncIOMotorClient(DATABASE_URI4)
db4 = client[DATABASE_NAME]
instance4 = Instance.from_db(db4)

@instance4.register
class Media4(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

#5th
client5 = AsyncIOMotorClient(DATABASE_URI5)
db5 = client[DATABASE_NAME]
instance5 = Instance.from_db(db5)

@instance5.register
class Media5(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

#6th
client6 = AsyncIOMotorClient(DATABASE_URI6)
db6 = client[DATABASE_NAME]
instance6 = Instance.from_db(db6)

@instance6.register
class Media6(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

async def choose_mediaDB():
    """This Function chooses which database to use based on the value of indexDB key in the dict tempDict."""
    global saveMedia
    if tempDict['indexDB'] == DATABASE_URI:
        logger.info("Using first db (Media)")
        saveMedia = Media
    elif tempDict['indexDB'] == DATABASE_URI2:
        logger.info("Using second db (Media2)")
        saveMedia = Media2
    elif tempDict['indexDB'] == DATABASE_URI3:
        logger.info("Using third db (Media3)")
        saveMedia = Media3
    elif tempDict['indexDB'] == DATABASE_URI4:
        logger.info("Using fourth db (Media4)")
        saveMedia = Media4
    elif tempDict['indexDB'] == DATABASE_URI5:
        logger.info("Using fifth db (Media5)")
        saveMedia = Media5
    elif tempDict['indexDB'] == DATABASE_URI6:
        logger.info("Using sixth db (Media6)")
        saveMedia = Media6
    else:
        logger.error("Invalid database URI specified in tempDict['indexDB']")


async def save_file_in_database(media):
    global saveMedia
    file_id, file_ref = unpack_new_file_id(media.file_id)
    file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
    DATABASES = [Media, Media2, Media3, Media4, Media5, Media6]
    try:
        for db in DATABASES:
            if await db.count_documents({'file_id': file_id}, limit=1):
                logger.warning(f'{getattr(media, "file_name", "NO_FILE")} is already saved in a database!')
                return False, 0
        file = saveMedia(
            file_id=file_id,
            file_ref=file_ref,
            file_name=file_name,
            file_size=media.file_size,
            file_type=media.file_type,
            mime_type=media.mime_type,
            caption=media.caption.html if media.caption else None,
        )
    except ValidationError:
        logger.exception('Error occurred while saving file in database')
        return False, 2
    else:
        try:
            await file.commit()
        except DuplicateKeyError:
            logger.warning(f'{getattr(media, "file_name", "NO_FILE")} is already saved in the database')
            return False, 0
        else:
            logger.info(f'{getattr(media, "file_name", "NO_FILE")} is saved to the database')
            return True, 1


async def get_search_results(query, file_type=None, max_results=8, offset=0, filter=False):
    """For given query return (results, next_offset)"""

    query = query.strip()

    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'(\b|[\.\+\-_]|\s|&)' + query + r'(\b|[\.\+\-_]|\s|&)'
    else:
        raw_pattern = query.replace(' ', r'.*[&\s\.\+\-_()\[\]]')

    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        return [], '', 0

    if USE_CAPTION_FILTER:
        filter = {'$or': [{'file_name': regex}, {'caption': regex}]}
    else:
        filter = {'file_name': regex}

    if file_type:
        filter['file_type'] = file_type
    
    # Query both collections
    cursor_media1 = Media.find(filter).sort('$natural', -1)
    cursor_media2 = Media2.find(filter).sort('$natural', -1)
    cursor_media3 = Media3.find(filter).sort('$natural', -1)
    cursor_media4 = Media4.find(filter).sort('$natural', -1)
    cursor_media5 = Media5.find(filter).sort('$natural', -1)
    cursor_media6 = Media6.find(filter).sort('$natural', -1)
    
    # Ensure offset is non-negative
    if offset < 0:
        offset = 0

    # Fetch files from both collections
    files_media1 = await cursor_media1.to_list(length=35)
    files_media2 = await cursor_media2.to_list(length=35)
    files_media3 = await cursor_media3.to_list(length=35)
    files_media4 = await cursor_media4.to_list(length=35)
    files_media5 = await cursor_media5.to_list(length=35)
    files_media6 = await cursor_media6.to_list(length=35)

    total_results = len(files_media1) + len(files_media2) + len(files_media3) + len(files_media4) + len(files_media5) + len(files_media6)
    # Interleave files from both collections based on the offset
    interleaved_files = []
    index_media1 = index_media2 = index_media3 = index_media4 = index_media5 = index_media6 = 0
    while index_media1 < len(files_media1) or index_media2 < len(files_media2) or index_media3 < len(files_media3) or index_media4 < len(files_media4) or index_media5 < len(files_media5) or index_media6 < len(files_media6):
        if index_media1 < len(files_media1):
            interleaved_files.append(files_media1[index_media1])
            index_media1 += 1
        if index_media2 < len(files_media2):
            interleaved_files.append(files_media2[index_media2])
            index_media2 += 1
        if index_media3 < len(files_media3):
            interleaved_files.append(files_media3[index_media3])
            index_media3 += 1
        if index_media4 < len(files_media4):
            interleaved_files.append(files_media4[index_media4])
            index_media4 += 1
        if index_media5 < len(files_media5):
            interleaved_files.append(files_media5[index_media5])
            index_media5 += 1
        if index_media6 < len(files_media6):
            interleaved_files.append(files_media6[index_media6])
            index_media6 += 1
    # Slice the interleaved files based on the offset and max_results
    files = interleaved_files[offset:offset + max_results]

    # Calculate next offset
    next_offset = offset + len(files)

    # If there are more results, return the next_offset; otherwise, set it to ''
    if next_offset < total_results:
        return files, next_offset, total_results
    else:
        return files, '', total_results
        
async def get_bad_files(query, file_type=None, filter=False):
    """For given query return (results, next_offset)"""
    query = query.strip()
    #if filter:
        #better ?
        #query = query.replace(' ', r'(\s|\.|\+|\-|_)')
        #raw_pattern = r'(\s|_|\-|\.|\+)' + query + r'(\s|_|\-|\.|\+)'
    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'(\b|[\.\+\-_])' + query + r'(\b|[\.\+\-_])'
    else:
        raw_pattern = query.replace(' ', r'.*[\s\.\+\-_()]')
    
    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        return []

    if USE_CAPTION_FILTER:
        filter = {'$or': [{'file_name': regex}, {'caption': regex}]}
    else:
        filter = {'file_name': regex}

    if file_type:
        filter['file_type'] = file_type

    cursor = Media.find(filter)
    cursor2 = Media2.find(filter)
    # Sort by recent
    cursor.sort('$natural', -1)
    cursor2.sort('$natural', -1)
    # Get list of files
    files = ((await cursor2.to_list(length=(await Media2.count_documents(filter))))+(await cursor.to_list(length=(await Media.count_documents(filter)))))

    #calculate total results
    total_results = len(files)

    return files, total_results

async def get_file_details(query):
    filter = {'file_id': query}
    cursor = Media.find(filter)
    filedetails = await cursor.to_list(length=1)
    if filedetails:
        return filedetails
    cursor_media2 = Media2.find(filter)
    filedetails_media2 = await cursor_media2.to_list(length=1)
    if filedetails_media2:
        return filedetails_media2
    cursor_media3 = Media3.find(filter)
    filedetails_media3 = await cursor_media3.to_list(length=1)
    if filedetails_media3:
        return filedetails_media3
    cursor_media4 = Media4.find(filter)
    filedetails_media4 = await cursor_media4.to_list(length=1)
    if filedetails_media4:
        return filedetails_media4
    cursor_media5 = Media5.find(filter)
    filedetails_media5 = await cursor_media5.to_list(length=1)
    if filedetails_media5:
        return filedetails_media5
    cursor_media6 = Media6.find(filter)
    filedetails_media6 = await cursor_media6.to_list(length=1)
    if filedetails_media6:
        return filedetails_media6


def encode_file_id(s: bytes) -> str:
    r = b""
    n = 0

    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0

            r += bytes([i])

    return base64.urlsafe_b64encode(r).decode().rstrip("=")


def encode_file_ref(file_ref: bytes) -> str:
    return base64.urlsafe_b64encode(file_ref).decode().rstrip("=")


def unpack_new_file_id(new_file_id):
    """Return file_id, file_ref"""
    decoded = FileId.decode(new_file_id)
    file_id = encode_file_id(
        pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash
        )
    )
    file_ref = encode_file_ref(decoded.file_reference)
    return file_id, file_ref
