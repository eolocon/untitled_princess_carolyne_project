from pydantic import BaseModel, Field
import datetime
from typing import List, Dict

""" Module containing Pydantic models to parse the scraping data """

class BaseDocument(BaseModel):
    document_type: str
    document_id: str
    document_url: str
    parent_document_id: str
    user_id: str
    username: str
    document_time: datetime.datetime
    document_text: str



class Post(BaseModel):
    document_type: str = Field(default='post')
    document_id: str = Field(alias='post_id')
    document_url: str = Field(alias='post_url')
    parent_document_id: str = Field(default=None)
    user_id: str
    username: str
    document_time: datetime.datetime = Field(alias='time')
    document_text: str = Field(alias='text')
    shares: str
    reactions: Dict[str, int]

class Comment(BaseModel):
    document_type: str = Field(default='comment')
    document_id: str = Field(alias='comment_id')
    document_url: str = Field(alias='comment_url')
    parent_document_id: str = Field(default=None)
    user_id: str = Field(alias='commenter_id')
    username: str = Field(alias='commenter_name')
    document_time: datetime.datetime = Field(alias='comment_time')
    document_text: str = Field(alias='comment_text')

class Reply(BaseModel):
    document_type: str = Field(default='reply')
    document_id: str = Field(alias='comment_id')
    document_url: str = Field(alias='comment_url')
    parent_document_id: str = Field(default=None)
    user_id: str = Field(alias='commenter_id')
    username: str = Field(alias='commenter_name')
    document_time: datetime.datetime = Field(alias='comment_time')
    document_text: str = Field(alias='comment_text')

