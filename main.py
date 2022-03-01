# Backend For EntertainmentVerse

# Imports
import math

from flask import Flask,render_template,request,flash,redirect,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
import json

# App
app=Flask(__name__)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/entertainment-verse'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.secret_key='saitama'

# DB
db=SQLAlchemy(app)

# Users Model
class Ev_users(db.Model):
    user_id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(255),nullable=False)
    user_email=db.Column(db.String(255),nullable=False)
    user_password=db.Column(db.String(255),nullable=False)
    user_added=db.Column(db.String(12),nullable=False)

# Movies Model
class Ev_movies(db.Model):
    movie_id=db.Column(db.Integer,primary_key=True)
    movie_slug=db.Column(db.String(255),nullable=False)
    movie_thumbnail=db.Column(db.String(255),nullable=False)
    movie_name=db.Column(db.String(255),nullable=False)
    movie_year=db.Column(db.String(4),nullable=True)
    movie_description=db.Column(db.String(255),nullable=True)
    movie_vid=db.Column(db.String(255),nullable=True)
    movie_genre=db.Column(db.String(255),nullable=True)
    movie_cast=db.Column(db.String(255),nullable=True)

# Animes Model
class Ev_animes(db.Model):
    anime_id=db.Column(db.Integer,primary_key=True)
    anime_slug=db.Column(db.String(255),nullable=False)
    anime_thumbnail=db.Column(db.String(255),nullable=False)
    anime_name=db.Column(db.String(255),nullable=False)
    anime_year=db.Column(db.String(4),nullable=True)
    anime_description=db.Column(db.String(255),nullable=True)
    anime_genre=db.Column(db.String(255),nullable=True)
    anime_episodes=db.Column(db.Integer,nullable=True)

# Web Series Model
class Ev_webseries(db.Model):
    webseries_id=db.Column(db.Integer,primary_key=True)
    webseries_slug=db.Column(db.String(255),nullable=False)
    webseries_thumbnail=db.Column(db.String(255),nullable=False)
    webseries_name=db.Column(db.String(255),nullable=False)
    webseries_year=db.Column(db.String(4),nullable=True)
    webseries_description=db.Column(db.String(255),nullable=True)
    webseries_genre=db.Column(db.String(255),nullable=True)
    webseries_episodes=db.Column(db.Integer,nullable=True)

# Animes Episodes Model
class Ev_anime_episodes(db.Model):
    episode_sno=db.Column(db.Integer,primary_key=True)
    episode_id=db.Column(db.Integer,nullable=False)
    anime_slug=db.Column(db.String(255),nullable=False)
    episode_slug=db.Column(db.String(255),nullable=False)
    episode_title=db.Column(db.String(255),nullable=False)
    episode_description=db.Column(db.String(255),nullable=True)
    episode_vid=db.Column(db.String(255),nullable=True)

# Web Series Episodes Model
class Ev_webseries_episodes(db.Model):
    episode_sno = db.Column(db.Integer, primary_key=True)
    episode_id=db.Column(db.Integer,nullable=False)
    webseries_slug=db.Column(db.String(255),nullable=False)
    episode_slug=db.Column(db.String(255),nullable=False)
    episode_title=db.Column(db.String(255),nullable=False)
    episode_description=db.Column(db.String(255),nullable=True)
    episode_vid=db.Column(db.String(255),nullable=True)

# Watchlist Model
class Ev_watchlist(db.Model):
    ev_id=db.Column(db.Integer,primary_key=True)
    ev_user_id=db.Column(db.Integer,nullable=False)
    ev_entertainment_type=db.Column(db.String(255),nullable=False)
    ev_entertainment_slug=db.Column(db.String(255),nullable=False)
    ev_entertainment_ep_slug=db.Column(db.String(255),nullable=True)
    ev_entertainment_ep_id=db.Column(db.Integer,nullable=True)
    ev_entertainment_ep_name=db.Column(db.String(255),nullable=True)
    ev_entertainment_thumbnail=db.Column(db.String(255),nullable=False)
    ev_entertainment_name=db.Column(db.String(255),nullable=False)
    ev_entertainment_year=db.Column(db.String(4),nullable=False)
    ev_entertainment_description=db.Column(db.String(255),nullable=False)
    ev_date_added=db.Column(db.String(12),nullable=False)

# Config.Json
with open('config.json') as c:
    params=json.load(c)['params']

# Home Page
@app.route('/')
def home():
    if 'uid' in session:
        return redirect('/latest-in-the-verse')
    else:
        if 'exists' in session:
            flash('User with this email id already exists','red-500')
            session.pop('exists')
        if 'wrong_pass' in session:
            flash('Wrong Password!','red-500')
            session.pop('wrong_pass')
        if 'no_account' in session:
            flash('No user account exists for this email id','red-500')
            session.pop('no_account')
        if 'need_to_login' in session:
            flash('You need to login first','red-500')
            session.pop('need_to_login')
        return render_template('index.html',title='A World of Entertainment',params=params)

# Login Post Request
@app.route('/login',methods=['POST'])
def login():
    if(request.method=='POST'):
        uemail=request.form.get('email')
        upass=request.form.get('password')

        check_user=Ev_users.query.filter_by(user_email=uemail).first()

        if(check_user):
            check_password=check_password_hash(check_user.user_password,upass)
            if(check_password):
                session['uid']=check_user.user_id
                session['login']=True
                return redirect('/latest-in-the-verse')
            else:
                session['wrong_pass']=True
                return redirect('/')
        else:
            session['no_account']=True
            return redirect('/')

# Signup Post Request
@app.route('/signup',methods=['POST'])
def signup():
    if(request.method=='POST'):
        uname=request.form.get('name')
        uemail=request.form.get('emailid')
        upass=generate_password_hash(request.form.get('upassword'))

        check_user=Ev_users.query.filter_by(user_email=uemail).all()

        if(check_user):
            session['exists']=True
            return redirect('/')
        else:
            add_user=Ev_users(user_name=uname,user_email=uemail,user_password=upass,user_added=datetime.now())
            db.session.add(add_user)
            db.session.commit()
            session['email']=uemail
            session['account_created']=True
            return redirect('/latest-in-the-verse')

# Post Login Page - Latest in the verse
@app.route('/latest-in-the-verse')
def latest():
    if 'uid' in session:
        if 'account_created' in session:
            flash('Account Created Successfully','green-500')
            session.pop('account_created')
        if 'login' in session:
            flash('Login Successful', 'green-500')
            session.pop('login')
        if 'new_pass_same_as_old' in session:
            flash('New Password cannot be same as Old Password','red-500')
            session.pop('new_pass_same_as_old')
        if 'old_pass_wrong' in session:
            flash('Incorrect Old Password','red-500')
            session.pop('old_pass_wrong')
        if 'pass_changed' in session:
            flash('Password Changed Successfully','green-500')
            session.pop('pass_changed')
        user=Ev_users.query.filter_by(user_id=session['uid']).first()
        user_watchlist = Ev_watchlist.query.filter_by(ev_user_id=user.user_id).all()
        badge=len(user_watchlist)
        latest_movies=Ev_movies.query.filter_by().order_by(desc(Ev_movies.movie_year)).all()[0:params['on_latest']]
        latest_animes=Ev_animes.query.filter_by().order_by(desc(Ev_animes.anime_year)).all()[0:params['on_latest']]
        latest_webseries=Ev_webseries.query.filter_by().order_by((Ev_webseries.webseries_year)).all()[0:params['on_latest']]
        return render_template('latest.html',title='Latest in the Verse',params=params,user=user,latest_movies=latest_movies,latest_animes=latest_animes,latest_webseries=latest_webseries,badge=badge)
    elif 'email' in session:
        userid=Ev_users.query.filter_by(user_email=session['email']).first()
        session['uid']=userid.user_id
        session.pop('email')
        return redirect('/latest-in-the-verse')
    else:
        session['need_to_login']=True
        return redirect('/')

# Entertainment Type Page
@app.route('/entertainment')
def entertainment():
    if 'uid' in session:
        user = Ev_users.query.filter_by(user_id=session['uid']).first()
        type=request.args.get('type')
        user_watchlist = Ev_watchlist.query.filter_by(ev_user_id=user.user_id).all()
        badge = len(user_watchlist)
        if(type=='Movies'):
            movies = Ev_movies.query.filter_by().all()
            total_pages = math.ceil(len(movies) / params['on_a_page'])
            page = request.args.get('page')
            if (page):
                page = int(page)
                movies = Ev_movies.query.filter_by().all()[(page - 1) * params['on_a_page']:page * params['on_a_page']]
                if(page==total_pages):
                    if((page-1)==1):
                        prev = '/entertainment?type=Movies'
                        next = 'javascript:void(0)'
                    else:
                        prev='/entertainment?type=Movies&page='+str(page-1)
                        next='javascript:void(0)'
                    return render_template('entertainment.html', title=type, params=params, user=user, movies=movies,page=page,prev=prev,next=next,badge=badge)
                else:
                    if ((page - 1) == 1):
                        prev = '/entertainment?type=Movies'
                        next = '/entertainment?type=Movies&page=' + str(page + 1)
                    else:
                        prev = '/entertainment?type=Movies&page=' + str(page - 1)
                        next = '/entertainment?type=Movies&page=' + str(page + 1)
                    return render_template('entertainment.html', title=type, params=params, user=user, movies=movies,page=page, prev=prev, next=next,badge=badge)
            else:
                prev='javascript:void(0)'
                next='/entertainment?type=Movies&page=2'
                movies = Ev_movies.query.filter_by().all()[0:params['on_a_page']]
                return render_template('entertainment.html',title=type,params=params,user=user,movies=movies,prev=prev,next=next,badge=badge)
        elif(type=='Animes'):
            animes = Ev_animes.query.filter_by().all()
            total_pages = math.ceil(len(animes) / params['on_a_page'])
            page = request.args.get('page')
            if (page):
                page = int(page)
                animes = Ev_animes.query.filter_by().all()[(page - 1) * params['on_a_page']:page * params['on_a_page']]
                if (page == total_pages):
                    if ((page - 1) == 1):
                        prev = '/entertainment?type=Animes'
                        next = 'javascript:void(0)'
                    else:
                        prev = '/entertainment?type=Animes&page=' + str(page - 1)
                        next = 'javascript:void(0)'
                    return render_template('entertainment.html', title=type, params=params, user=user, animes=animes,
                                           page=page, prev=prev, next=next,badge=badge)
                else:
                    if ((page - 1) == 1):
                        prev = '/entertainment?type=Animes'
                        next = '/entertainment?type=Animes&page=' + str(page + 1)
                    else:
                        prev = '/entertainment?type=Animes&page=' + str(page - 1)
                        next = '/entertainment?type=Animes&page=' + str(page + 1)
                    return render_template('entertainment.html', title=type, params=params, user=user, animes=animes,
                                           page=page, prev=prev, next=next,badge=badge)
            else:
                prev = 'javascript:void(0)'
                next = '/entertainment?type=Animes&page=2'
                animes = Ev_animes.query.filter_by().all()[0:params['on_a_page']]
                return render_template('entertainment.html', title=type, params=params, user=user, animes=animes,prev=prev, next=next,badge=badge)
        else:
            webseriesall = Ev_webseries.query.filter_by().all()
            total_pages = math.ceil(len(webseriesall) / params['on_a_page'])
            page = request.args.get('page')
            if (page):
                page = int(page)
                webserie = Ev_webseries.query.filter_by().all()[(page - 1) * params['on_a_page']:page * params['on_a_page']]
                if (page == total_pages):
                    if ((page - 1) == 1):
                        prev = '/entertainment?type=Web-Series'
                        next = 'javascript:void(0)'
                    else:
                        prev = '/entertainment?type=Web-Series&page=' + str(page - 1)
                        next = 'javascript:void(0)'
                    return render_template('entertainment.html', title=type, params=params, user=user, webserie=webserie,
                                           page=page, prev=prev, next=next,badge=badge)
                else:
                    if ((page - 1) == 1):
                        prev = '/entertainment?type=Web-Series'
                        next = '/entertainment?type=Web-Series&page=' + str(page + 1)
                    else:
                        prev = '/entertainment?type=Web-Series&page=' + str(page - 1)
                        next = '/entertainment?type=Web-Series&page=' + str(page + 1)
                    return render_template('entertainment.html', title=type, params=params, user=user, webserie=webserie,
                                           page=page, prev=prev, next=next,badge=badge)
            else:
                if 'already_added' in session:
                    flash('Already in your Watchlist', 'red-500')
                    session.pop('already_added')
                prev = 'javascript:void(0)'
                next = '/entertainment?type=Web-Series&page=2'
                webserie = Ev_webseries.query.filter_by().all()[0:params['on_a_page']]
                return render_template('entertainment.html', title=type, params=params, user=user, webserie=webserie,
                                       prev=prev, next=next,badge=badge)

    else:
        session['need_to_login'] = True
        return redirect('/')

# Change Password
@app.route('/change-password',methods=['POST'])
def changepass():
    if 'uid' in session:
        user = Ev_users.query.filter_by(user_id=session['uid']).first()
        if(request.method=='POST'):
            old_pass=request.form.get('oldpassword')
            new_pass=request.form.get('newpassword')
            cnew_pass=request.form.get('cnpassword')
            check_old_pass=check_password_hash(user.user_password,old_pass)
            if(check_old_pass):
                check_new_pass=check_password_hash(user.user_password,new_pass)
                if(check_new_pass):
                    # return 'new'
                    session['new_pass_same_as_old'] = True
                    return redirect('/latest-in-the-verse')
                else:
                    user.user_password=generate_password_hash(new_pass)
                    db.session.commit()
                    session['pass_changed'] = True
                    # return 'ok'
                    return redirect('/latest-in-the-verse')
            else:
                # return 'old'
                session['old_pass_wrong']=True
                return redirect('/latest-in-the-verse')

    else:
        session['need_to_login'] = True
        return redirect('/')

# Episodes List
@app.route('/episodes/<string:name>/<string:slug>')
def episodes(name,slug):
    if 'uid' in session:
        user = Ev_users.query.filter_by(user_id=session['uid']).first()
        user_watchlist = Ev_watchlist.query.filter_by(ev_user_id=user.user_id).all()
        badge = len(user_watchlist)
        if(name=='anime'):
            if 'already_added' in session:
                flash('Already in your Watchlist','red-500')
                session.pop('already_added')
            anime=Ev_animes.query.filter_by(anime_slug=slug).first()
            episodes=Ev_anime_episodes.query.filter_by(anime_slug=slug).all()
            return render_template('episodes.html',title=anime.anime_name,params=params,user=user,name=name,anime=anime,episodes=episodes,badge=badge)
        else:
            if 'already_added' in session:
                flash('Already in your Watchlist','red-500')
                session.pop('already_added')
            webseries=Ev_webseries.query.filter_by(webseries_slug=slug).first()
            episodes=Ev_webseries_episodes.query.filter_by(webseries_slug=slug).all()
            return render_template('episodes.html',title=webseries.webseries_name,params=params,user=user,name=name,webseries=webseries,episodes=episodes,badge=badge)
    else:
        session['need_to_login'] = True
        return redirect('/')

# Watch page
@app.route('/watch/<string:name>/<string:slug>')
def watch(name,slug):
    if 'uid' in session:
        user = Ev_users.query.filter_by(user_id=session['uid']).first()
        user_watchlist = Ev_watchlist.query.filter_by(ev_user_id=user.user_id).all()
        badge = len(user_watchlist)
        if(name=='movie'):
            if 'already_added' in session:
                flash('Already in your Watchlist','red-500')
                session.pop('already_added')
            movie=Ev_movies.query.filter_by(movie_slug=slug).first()
            return render_template('watch.html',title=movie.movie_name,params=params,user=user,name=name,movie=movie,badge=badge)
        elif (name == 'anime'):
            if 'already_added' in session:
                flash('Already in your Watchlist','red-500')
                session.pop('already_added')
            anime_title = request.args.get('title')
            episode_number = request.args.get('episode')
            anime = Ev_animes.query.filter_by(anime_slug=anime_title).first()
            episodes=Ev_anime_episodes.query.filter_by(anime_slug=anime_title).all()
            total_episodes=len(episodes)
            episode_number = int(episode_number)
            episode = Ev_anime_episodes.query.filter_by(anime_slug=anime_title,episode_id=episode_number).first()
            if(episode_number==1):
                ep_number=episode_number+1
                ep = Ev_anime_episodes.query.filter_by(anime_slug=anime_title,episode_id=ep_number).first()
                prev='javascript:void(0)'
                next=(f"/watch/anime/{ep.episode_slug}?title={anime_title}&episode={str(episode_number+1)}")
            elif(episode_number==total_episodes):
                ep_number = episode_number - 1
                ep = Ev_anime_episodes.query.filter_by(anime_slug=anime_title,episode_id=ep_number).first()
                prev = (f"/watch/anime/{ep.episode_slug}?title={anime_title}&episode={str(episode_number-1)}")
                next = 'javascript:void(0)'
            else:
                ep_number_prev = episode_number - 1
                ep_prev = Ev_anime_episodes.query.filter_by(anime_slug=anime_title,episode_id=ep_number_prev).first()
                ep_number_next = episode_number + 1
                ep_next = Ev_anime_episodes.query.filter_by(anime_slug=anime_title,episode_id=ep_number_next).first()
                prev = (f"/watch/anime/{ep_prev.episode_slug}?title={anime_title}&episode={str(episode_number-1)}")
                next = (f"/watch/anime/{ep_next.episode_slug}?title={anime_title}&episode={str(episode_number+1)}")
            return render_template('watch.html', title=episode.episode_title, params=params, user=user, name=name,anime=anime,episode=episode,next=next,prev=prev,anime_title=anime_title,episode_number=episode_number,badge=badge)
        else:
            if 'already_added' in session:
                flash('Already in your Watchlist','red-500')
                session.pop('already_added')
            webseries_title = request.args.get('title')
            episode_number = request.args.get('episode')
            webseries = Ev_webseries.query.filter_by(webseries_slug=webseries_title).first()
            episodes=Ev_webseries_episodes.query.filter_by(webseries_slug=webseries_title).all()
            total_episodes=len(episodes)
            episode_number = int(episode_number)
            episode = Ev_webseries_episodes.query.filter_by(webseries_slug=webseries_title,episode_id=episode_number).first()
            if(episode_number==1):
                ep_number=episode_number+1
                ep = Ev_webseries_episodes.query.filter_by(webseries_slug=webseries_title,episode_id=ep_number).first()
                prev='javascript:void(0)'
                next=(f"/watch/webseries/{ep.episode_slug}?title={webseries_title}&episode={str(episode_number+1)}")
            elif(episode_number==total_episodes):
                ep_number = episode_number - 1
                ep = Ev_webseries_episodes.query.filter_by(webseries_slug=webseries_title,episode_id=ep_number).first()
                prev = (f"/watch/webseries/{ep.episode_slug}?title={webseries_title}&episode={str(episode_number-1)}")
                next = 'javascript:void(0)'
            else:
                ep_number_prev = episode_number - 1
                ep_prev = Ev_webseries_episodes.query.filter_by(webseries_slug=webseries_title,episode_id=ep_number_prev).first()
                ep_number_next = episode_number + 1
                ep_next = Ev_webseries_episodes.query.filter_by(webseries_slug=webseries_title,episode_id=ep_number_next).first()
                prev = (f"/watch/webseries/{ep_prev.episode_slug}?title={webseries_title}&episode={str(episode_number-1)}")
                next = (f"/watch/webseries/{ep_next.episode_slug}?title={webseries_title}&episode={str(episode_number+1)}")
            return render_template('watch.html', title=episode.episode_title, params=params, user=user, name=name,
                                   webseries=webseries,episode=episode,next=next,prev=prev,webseries_title=webseries_title,episode_number=episode_number,badge=badge)
    else:
        session['need_to_login'] = True
        return redirect('/')

# Search Page Get Request
@app.route('/search')
def search():
    if 'uid' in session:
        search_queryi=request.args.get('query')
        user = Ev_users.query.filter_by(user_id=session['uid']).first()
        user_watchlist = Ev_watchlist.query.filter_by(ev_user_id=user.user_id).all()
        badge = len(user_watchlist)
        search_querym = search_queryi + '%'
        search_queryf = '%' + search_querym
        movies = Ev_movies.query.filter(Ev_movies.movie_name.like(search_queryf)).all()
        animes = Ev_animes.query.filter(Ev_animes.anime_name.like(search_queryf)).all()
        webseries = Ev_webseries.query.filter(Ev_webseries.webseries_name.like(search_queryf)).all()
        return render_template('search.html', title='Search ' + search_queryi, params=params, user=user, movies=movies,
                               animes=animes, webserie=webseries,badge=badge)
    else:
        session['need_to_login'] = True
        return redirect('/')

# Search Page Post Request
@app.route('/query',methods=['GET','POST'])
def query():
    if 'uid' in session:
        user = Ev_users.query.filter_by(user_id=session['uid']).first()
        user_watchlist = Ev_watchlist.query.filter_by(ev_user_id=user.user_id).all()
        badge = len(user_watchlist)
        if(request.method=='POST'):
            search_queryi=request.form.get('search')
            return redirect(f"/search?query={search_queryi}")
    else:
        session['need_to_login'] = True
        return redirect('/')

# My Watchlist Page
@app.route('/my-watchlist')
def watchlist():
    if 'uid' in session:
        if 'removed_from_watchlist' in session:
            flash('Removed from Watchlist','green-500')
            session.pop('removed_from_watchlist')
        if 'added_to_watchlist' in session:
            flash('Added to Watchlist', 'green-500')
            session.pop('added_to_watchlist')
        user = Ev_users.query.filter_by(user_id=session['uid']).first()
        watch_list=Ev_watchlist.query.filter_by(ev_user_id=user.user_id).all()
        badge = len(watch_list)
        return render_template('watchlist.html',title='My Watchlist',params=params,user=user,watch_list=watch_list,badge=badge)
    else:
        session['need_to_login'] = True
        return redirect('/')

# Add To Watchlist Post Request
@app.route('/add-to-watchlist')
def add_watchlist():
    if 'uid' in session:
        user = Ev_users.query.filter_by(user_id=session['uid']).first()
        user_watchlist = Ev_watchlist.query.filter_by(ev_user_id=user.user_id).all()
        badge = len(user_watchlist)
        type=request.args.get('type')
        ent_slug=request.args.get('slug')
        if(type=='movie'):
            check=Ev_watchlist.query.filter_by(ev_user_id=user.user_id,ev_entertainment_slug=ent_slug).all()
            # print(check)
            if(check):
                session['already_added']=True
                return redirect(f"/watch/{type}/{ent_slug}")
            else:
                movie=Ev_movies.query.filter_by(movie_slug=ent_slug).first()
                add_to_watchlist=Ev_watchlist(ev_user_id=user.user_id,ev_entertainment_type=type,ev_entertainment_slug=ent_slug,ev_entertainment_thumbnail=movie.movie_thumbnail,ev_entertainment_name=movie.movie_name,ev_entertainment_year=movie.movie_year,ev_entertainment_description=movie.movie_description,ev_date_added=datetime.now())
                db.session.add(add_to_watchlist)
                db.session.commit()
                session['added_to_watchlist']=True
                return redirect('/my-watchlist')
        elif (type == 'anime'):
            epslug = request.args.get('epslug')
            epid = request.args.get('epid')
            check = Ev_watchlist.query.filter_by(ev_user_id=user.user_id, ev_entertainment_slug=ent_slug,
                                                 ev_entertainment_ep_slug=epslug).all()
            if (check):
                session['already_added'] = True
                return redirect(f"/watch/{type}/{epslug}?title={ent_slug}&episode={epid}")
            else:
                ep = Ev_anime_episodes.query.filter_by(episode_slug=epslug).first()
                anim = Ev_animes.query.filter_by(anime_slug=ent_slug).first()
                add_to_watchlist = Ev_watchlist(ev_user_id=user.user_id, ev_entertainment_type=type,
                                                ev_entertainment_slug=ent_slug, ev_entertainment_ep_slug=epslug,
                                                ev_entertainment_ep_id=epid, ev_entertainment_ep_name=ep.episode_title,
                                                ev_entertainment_thumbnail=anim.anime_thumbnail,
                                                ev_entertainment_name=anim.anime_name,
                                                ev_entertainment_year=anim.anime_year,
                                                ev_entertainment_description=anim.anime_description,
                                                ev_date_added=datetime.now())
                db.session.add(add_to_watchlist)
                db.session.commit()
                session['added_to_watchlist'] = True
                return redirect('/my-watchlist')
        elif (type == 'webseries'):
            epslug = request.args.get('epslug')
            epid = request.args.get('epid')
            check = Ev_watchlist.query.filter_by(ev_user_id=user.user_id, ev_entertainment_slug=ent_slug,
                                                 ev_entertainment_ep_slug=epslug).all()
            if (check):
                session['already_added'] = True
                return redirect(f"/watch/{type}/{epslug}?title={ent_slug}&episode={epid}")
            ep = Ev_webseries_episodes.query.filter_by(episode_slug=epslug).first()
            webserie = Ev_webseries.query.filter_by(webseries_slug=ent_slug).first()
            add_to_watchlist = Ev_watchlist(ev_user_id=user.user_id, ev_entertainment_type=type,
                                            ev_entertainment_slug=ent_slug, ev_entertainment_ep_slug=epslug,
                                            ev_entertainment_ep_id=epid, ev_entertainment_ep_name=ep.episode_title,
                                            ev_entertainment_thumbnail=webserie.webseries_thumbnail,
                                            ev_entertainment_name=webserie.webseries_name,
                                            ev_entertainment_year=webserie.webseries_year,
                                            ev_entertainment_description=webserie.webseries_description,
                                            ev_date_added=datetime.now())
            db.session.add(add_to_watchlist)
            db.session.commit()
            session['added_to_watchlist'] = True
            return redirect('/my-watchlist')
        elif(type=='anime_episodes'):
            check = Ev_watchlist.query.filter_by(ev_user_id=user.user_id, ev_entertainment_slug=ent_slug,ev_entertainment_ep_slug=None).all()
            if(check):
                session['already_added'] = True
                return redirect(f"/episodes/anime/{ent_slug}")
            else:
                epi=Ev_animes.query.filter_by(anime_slug=ent_slug).first()
                add_to_watchlist=Ev_watchlist(ev_user_id=user.user_id,ev_entertainment_type=type,ev_entertainment_slug=ent_slug,ev_entertainment_thumbnail=epi.anime_thumbnail,ev_entertainment_name=epi.anime_name,ev_entertainment_year=epi.anime_year,ev_entertainment_description=epi.anime_description,ev_date_added=datetime.now())
                db.session.add(add_to_watchlist)
                db.session.commit()
                session['added_to_watchlist']=True
                return redirect('/my-watchlist')
        elif(type=='webseries_episodes'):
            check = Ev_watchlist.query.filter_by(ev_user_id=user.user_id, ev_entertainment_slug=ent_slug,ev_entertainment_ep_slug=None).all()
            if (check):
                session['already_added'] = True
                return redirect(f"/episodes/webseries/{ent_slug}")
            else:
                epi=Ev_webseries.query.filter_by(webseries_slug=ent_slug).first()
                add_to_watchlist=Ev_watchlist(ev_user_id=user.user_id,ev_entertainment_type=type,ev_entertainment_slug=ent_slug,ev_entertainment_thumbnail=epi.webseries_thumbnail,ev_entertainment_name=epi.webseries_name,ev_entertainment_year=epi.webseries_year,ev_entertainment_description=epi.webseries_description,ev_date_added=datetime.now())
                db.session.add(add_to_watchlist)
                db.session.commit()
                session['added_to_watchlist']=True
                return redirect('/my-watchlist')
    else:
        session['need_to_login'] = True
        return redirect('/')

@app.route('/delete-from-watchlist')
def delete():
    type=request.args.get('type')
    user_watchlist = Ev_watchlist.query.filter_by(ev_user_id=user.user_id).all()
    badge = len(user_watchlist)
    if(type=='movie'):
        ent=request.args.get('ent')
        remove=Ev_watchlist.query.filter_by(ev_entertainment_slug=ent).first()
        db.session.delete(remove)
        db.session.commit()
        session['removed_from_watchlist']=True
        return redirect('/my-watchlist')
    elif(type=='anime_episodes'):
        ent=request.args.get('ent')
        remove=Ev_watchlist.query.filter_by(ev_entertainment_type=type,ev_entertainment_slug=ent).first()
        db.session.delete(remove)
        db.session.commit()
        session['removed_from_watchlist']=True
        return redirect('/my-watchlist')
    elif(type=='webseries_episodes'):
        ent=request.args.get('ent')
        remove=Ev_watchlist.query.filter_by(ev_entertainment_type=type,ev_entertainment_slug=ent).first()
        db.session.delete(remove)
        db.session.commit()
        session['removed_from_watchlist']=True
        return redirect('/my-watchlist')
    else:
        ent=request.args.get('entep')
        remove = Ev_watchlist.query.filter_by(ev_entertainment_ep_slug=ent).first()
        db.session.delete(remove)
        db.session.commit()
        session['removed_from_watchlist']=True
        return redirect('/my-watchlist')

# Logout
@app.route('/logout')
def logout():
    session.pop('uid')
    return redirect('/')

# App Run
app.run(debug=True)

# # Watch Anime,Web Series page
# @app.route('/watch/<string:name>')
# def watch(name):
#     if 'uid' in session:
#         user = Ev_users.query.filter_by(user_id=session['uid']).first()
#         if (name == 'anime'):
#             anime_title = request.args.get('title')
#             episode_number = request.args.get('episode')
#             anime = Ev_animes.query.filter_by(anime_slug=anime_title).first()
#             episodes=Ev_anime_episodes.query.filter_by(anime_slug=anime_title).all()
#             total_episodes=len(episodes)
#             print(total_episodes)
#             episode = Ev_anime_episodes.query.filter_by(episode_id=episode_number, anime_slug=anime_title).first()
#             if(episode_number=='1'):
#                 episode_number=int(episode_number)
#                 prev='javascript:void(0)'
#                 next = '/watch/anime?title=one-punch-man&episode='+str(episode_number+1)
#             elif(episode_number==total_episodes):
#                 episode_number=int(episode_number)
#                 prev = '/watch/anime?title=one-punch-man&episode=' + str(episode_number - 1)
#                 next = 'javascript:void(0)'
#             else:
#                 episode_number = int(episode_number)
#                 prev = '/watch/anime?title=one-punch-man&episode=' + str(episode_number - 1)
#                 next = '/watch/anime?title=one-punch-man&episode=' + str(episode_number + 1)
#             return render_template('watch.html', title=episode.episode_title, params=params, user=user, name=name,
#                                    anime=anime,episode=episode,next=next,prev=prev,anime_title=anime_title)
#     else:
#         session['need_to_login'] = True
#         return redirect('/')

