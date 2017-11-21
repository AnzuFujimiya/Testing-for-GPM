#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
from builtins import * # noqa

from gmusicapi import Mobileclient
from getpass import getpass

import importlib

import subprocess

import codecs

import urllib2

import vlc

import json

import time

import os

# JSON attribute
class D(dict):
	__getattr__ = dict.__getitem__

#get API
def ask_for_credentials():

	api = Mobileclient()

	logged_in = False
	attempts = 0

	while not logged_in and attempts < 3:
		email = input('Email: ')
		password = getpass()

		try:
			logged_in = api.login(email, password, Mobileclient.FROM_MAC_ADDRESS)
		except:
			print()

		attempts += 1

	return api


#api check
def play():
	api = ask_for_credentials()

	if not api.is_authenticated():
		print("Sorry, those credentials weren't accepted.")
		return

	print('Successfully logged in.\n')

	show_info(api)

#get all list
def show_info(api):

	print('Loading library...',end=' ')
	library = api.get_all_songs()
	print('Done.')

	print(len(library), 'tracks detected.\n')

	libraryjson = json.dumps(library)
	libraryjson = json.loads(libraryjson, object_hook=D)
	''' ライブラリ全曲をjsonに書き出し
	with codecs.open('test.json', 'w', 'utf-8') as f:
		json.dump(libraryjson, f,
			indent=4,
			ensure_ascii=False,
			sort_keys=True)
	'''
	# AlbumArtRefが存在するかどうがチェック
	for song in libraryjson:
		missing = 0
		if not 'AlbumArtRef' in song:
			missing += 1
			print('Album art not found')
		if not 'ArtistArtRef' in song:
			missng += 2
			print('Artist art not found')
		if missing > 0:
			print('Searching for artworks..')
			find_art(song, missing)



	'''
	while(True):
		# print_art_info(libraryjson,index)
		cmd = input("\nPress \'Enter\' to see info\nPress \'s\' to show next song\nPress \'e\' to exit.\n")
		if cmd == 'e':
			api.logout()
			print('Exitting..')
			exit()

		elif cmd == 's':
			show_info(api)
	'''

#find pics from google
def find_art(song, missing):
	gSearch = importlib.import_module("google-images-download")
	if missing >= 2:
		try:
			urls = url_search(song.artist,n=5)
			url_download(song.artist, urls)
			missing -= 2
		except:
			print("Cannot find artist name.")
	if missing >= 1:
		try:
			keyword = song.title+" "+song.artist
			urls = url_search(keyword,n=5)
			url_download(keyword, urls)
			missing -= 1
		except:
			print("Cannot find song title.")

def url_search(keyword, n):
	img_url=[]
	url = "http://ajax.googleapis.com/ajax/services/search/images?q={0}&amp;v=1.0&amp;rsz=middle&amp;start={1}"
	for i in range((n/8)+1):
		res = urllib2.urlopen(url.format(keyword,i*8))
		data = json.load(res)
		img_url += [result["url"] for result in data["responseData"]["results"]]
	return img_url

def url_download(keyword,urls):
	print("Download start..")
	# make directory to store image (if not exists)
	if os.path.exists(keyword)==False
		os.mkdir(keyword)

	opener = urllib2.build_opener()

	for i in range(len(set(urls))):
		try:
			fn, ext = os.path.splitext(urls[i])
			req = urllib2.Request(urls[i], headers={"User-Agent" : "Magic Browser"})
			img_file = open(keyword+"/"+str(i)+ext, "wb")
			img_file.write(opener.open(req).read())
			img_file.close()
			print("DL Image Link:"+str(i+1))
		except:
			continue

#print info
def print_song_info(song, Art_Exists=True):
	print()
	album = song.album
	artist = song.artist
	title = song.title
	if Art_Missing:
		albumUrl = song.albumArtRef.url
		artistUrl = song.artistArtRef.url

	print("Title: {}".format(title))
	print("Artist: {}".format(artist))
	print("Album: {}".format(album))
	if Art_Missing:
		print("AlbumURL: {}".format(albumUrl))
		print("ArtistURL: {}".format(artistUrl))

if __name__ == '__main__':
	play()






