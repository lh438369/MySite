from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserInfo(AbstractUser):
    #用户表
    nid=models.AutoField(primary_key=True)
    nickname=models.CharField(verbose_name="昵称",max_length=32)
    telephone=models.CharField(max_length=11,blank=True,null=True,unique=True,verbose_name="手机号")
    avatar=models.FileField(verbose_name="头像",upload_to="avatar/",default="avatar/default.png")
    create_time=models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    blog=models.OneToOneField(to="Blog",to_field="nid",null=True)
    def __str__(self):
        return self.username


class Blog(models.Model):
    #个人博客表
    nid=models.AutoField(primary_key=True)
    title=models.CharField(verbose_name="个人博客标题",max_length=64)
    stie=models.CharField(verbose_name="个人博客后缀",max_length=32,unique=True)
    theme=models.CharField(verbose_name="博客主题",max_length=32)
    def __str__(self):
        return self.title

class HomeCategory(models.Model):
    #文章分类表
    nid = models.AutoField(primary_key=True)
    title=models.CharField(verbose_name="分类标题",max_length=32)
    blog=models.ForeignKey(verbose_name="所属博客",to="Blog",to_field="nid")
    def __str__(self):
        return self.title

class Article(models.Model):
    #文章表
    nid=models.AutoField(primary_key=True)
    title=models.CharField(verbose_name="文章标题",max_length=50)
    desc=models.CharField(max_length=255,verbose_name="文章描述")
    read_count=models.IntegerField(default=0)
    comment_count=models.IntegerField(default=0)
    up_count=models.IntegerField(default=0)
    down_count=models.IntegerField(default=0)
    create_time=models.DateTimeField(verbose_name="创建时间")
    homecategory=models.ForeignKey(verbose_name="文章类型",to="HomeCategory",to_field="nid")
    user=models.ForeignKey(verbose_name="作者",to="UserInfo",to_field="nid")
    tags=models.ManyToManyField(verbose_name="文章标签",to="Tag",through="Article2Tag",through_fields=("article","tag"))
    def __str__(self):
        return self.title


class Tag(models.Model):
    # 文章标签表
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="标签名称", max_length=32)
    blog = models.ForeignKey(verbose_name="所属博客", to="Blog", to_field="nid")

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    #文章标签对应表（多对多产生的第三张表）
    nid = models.AutoField(primary_key=True)
    article=models.ForeignKey(verbose_name="文章",to="Article",to_field="nid")
    tag=models.ForeignKey(verbose_name="标签",to="Tag",to_field="nid")
    def __str__(self):
        return self.article.title+"---"+self.tag.title


class ArticleDetail(models.Model):
    #文章详细表
    nid=models.AutoField(primary_key=True)
    content=models.TextField(verbose_name="文章内容")
    article=models.OneToOneField(verbose_name="所属文章",to="Article",to_field="nid")


class Comment(models.Model):
    #评论表
    nid=models.AutoField(primary_key=True)
    article=models.ForeignKey(verbose_name="评论文章",to="Article",to_field="nid")
    content=models.CharField(verbose_name="评论的内容",max_length=255)
    create_time=models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    parent_comment=models.ForeignKey("self",blank=True,null=True,verbose_name="父级评论")
    user=models.ForeignKey(verbose_name="评论者",to="UserInfo",to_field="nid")
    up_count=models.IntegerField(default=0)
    def __str__(self):
        return self.content

class ArticleUpDown(models.Model):
    #文章点赞及反对表
    nid=models.AutoField(primary_key=True)
    user=models.ForeignKey("UserInfo",null=True)
    article=models.ForeignKey("Article",null=True)
    is_up=models.BooleanField(default=True,verbose_name="是否赞")

class CommentUp(models.Model):
    #评论点赞表
    nid=models.AutoField(primary_key=True)
    user=models.ForeignKey("UserInfo",null=True)
    comment=models.ForeignKey("Comment",null=True)




