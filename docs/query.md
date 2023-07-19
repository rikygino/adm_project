# Queries DataBase

1) Given a user, find all the songs and the titles of the songs that the given user likes

        db.users.aggregate([
            { $match: { user_id: 42 } },
            { $unwind: "$likedSongs" },
            { $project: { _id: 0, song_id: "$likedSongs.song_id", title: "$likedSongs.title"}}
        ])

2) Given a user find all his playlist and their name, and the number of songs in each one

        db.users.aggregate([
            { $match: { user_id: 5 } },
            { $unwind: "$playlists" },
            { $project: { _id: 0, playlist_id: "$playlists.playlist_id", 
             playlist_name: "$playlists.playlist_name", num_songs: { $size: "$playlists.songs" } } }
        ])
3) Given an account find all user associated with it and their username

        db.accountss.aggregate([
           { $match: { "account_id": 10 } },
           { $unwind: "$users" },
           { $project: { "_id": 0,"user_id": "$users.user_id", "username": "$users.username" } }
        ])

4) Given a playlist, find the name of the user who created it and the name of the songs contained

        db.playlists.aggregate([
           { $match: { "playlist_id": 19 } },
           { $project: { "_id": 0, "username": "$username", "song_names": "$songs.title" }} 
        ])

5) Given a song find all its information (album & artist)

        db.songs.find({ "song_id": 1 })
6) Given a song find the average age of users who liked it

        db.songs.aggregate([
           { $match: { "song_id": 8 } },
           { $unwind: "$users" },
           {
             $group: {
               "_id": 0,
               "average_age": {
                 $avg: {
                   $divide: [
                     {
                       $subtract: [new Date(), "$users.birthdate"]
                     },
                     1000 * 60 * 60 * 24 * 365.25
                   ]
                 }
               }
             }
           },
           {
             $project: {
               "_id": 0,
               "average_age": { $floor: "$average_age" }
             }
           }])
   
7) Given an artist find the title of his albums and the titles of the songs in each of them.

        db.artists.aggregate([
           { $match: { "artist_id": 50} },
           { $unwind: "$songs" },
           { $project: { "_id": 0, "album_title": "$songs.album_name", "song_titles": "$songs.title"   }}
        ])

8) Given an artist find his 3 most liked songs by users

        db.artists.aggregate([
           { $match: { artist_id: 50 } },
           { $unwind: "$songs" },
           { $addFields: {
             likedCount: { $size: "$songs.users" }
           } },
           { $sort: { likedCount: -1 } },
           { $limit: 3 },
           { $project: {
             _id: 0,
             song_id: "$songs.song_id",
             title: "$songs.title",
             likedCount: 1
           } }
        ])

9) Given a playlist find the average danceability of its songs

        db.playlists.aggregate([
          { $match: { "playlist_id": 71 } },
          { $unwind: "$songs" },
          { $group: {
              _id: null,
              average_danceability: { $avg: "$songs.danceability" }
            }
          },
          { $project: {
              _id: 0,
              average_danceability: { $round: ["$average_danceability", 2] }
            }
          }
        ])

10) Find the name and surname of the accounts whose subscription is expired 

        db.subscriptions.aggregate([
           {
             $match: {
               expiration_date: { $lt: new Date() }
             }
           },
           {
             $project: {
               _id: 0,
               name: "$name",
               surname: "$surname"
             }
           }
        ])

11) Given an artist find all his albums titles sorted by year

        db.artists.aggregate([
           { $match: { artist_id: 33 } },
           { $unwind: "$songs" },
           { $group: { 
               _id: "$songs.album_id",
               album_title: { $first: "$songs.album_name" }, 
               year: { $first: "$songs.year" } } },
           { $sort: { year: 1 } },
           { $project: {
               _id: 0,
               album_title: 1
             }
           }
         ])

12) Given a playlist find the duration of it
    
        db.playlists.aggregate([
           { $match: { "playlist_id": 30 } },
           { $unwind: "$songs" },
           { $group: {
               _id: "$_id",
               duration: { $sum: "$songs.duration" }
             }
           },
           { $project: {
               _id: 0,
               durationInMinutes: { $divide: ["$duration", 1000 * 60] }
             }}])
13) Given an album find the artist, the title and the duration of each song in it

        db.albums.aggregate([
            { $match: { "album_id": 47 } },
            { $unwind: "$songs" },
            {
              $project: {
                _id: 0,
                artist: "$songs.createdByArtists.artist_name",
                song: "$songs.title",
                duration: {
                  $round: [{ $divide: ["$songs.duration", 60000] },2]
                }
              }
            }
        ])
14) Given an account show email, subscription type and start date of the subscription

        db.accountss.aggregate([
          { $match: { "account_id": 24 } },
          { $project: {
            "_id": 0,
            "email": "$email",
            "subscription_type": "$subscription_type",
            "start_date": "$start_date"
          }}
        ])
15) Given an artist and a user show the title of all the songs of this artist like by the user

        db.artists.aggregate([
           { $match: { "artist_id": 1 } },
           { $unwind: "$songs" },
           { $match: { "songs.users.user_id": 3756 } },
           { $project: {
             "_id": 0,
             "song_title": "$songs.title"
           }}
         ])
                
16) Given a song and an account, show the name of all the playlist of this account that contain the song

        db.accountss.aggregate([
          { $match: {
              "users.playlists.songs.song_id": 357,
              account_id: 1
            }},
          { $unwind: "$users"},
          { $unwind: "$users.playlists" },
          { $match: {
              "users.playlists.songs.song_id": 357}},
          { $project: {
              _id: 0,
              playlist_name: "$users.playlists.playlist_name"
            }}
        ])

