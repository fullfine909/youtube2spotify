# Youtube2Spotify
Youtube2Spotify is a tool designed to get Spotify playlists from YouTube videos of DJ sets. As a lover of electronic music, I enjoy listening to dj sets and many times I come across songs that I would like to add to my music library. Now this task is much easier for me thanks to this tool.

# Try it right now!
- http://newys-env.eba-zuczgtaa.eu-west-1.elasticbeanstalk.com/

Examples to test it:
- https://www.youtube.com/watch?v=4utKO75DtBE&feature=youtu.be&ab_channel=BE-AT.TV
- https://www.youtube.com/watch?v=DJsbzQqYUd0&t=2411s&ab_channel=H%C3%96RBERLIN
- https://www.youtube.com/watch?v=XRotY7PuWMc&feature=youtu.be&ab_channel=BoilerRoom

# Features
- Link to Spotify for each song
- Useful information for deejays as BPM
- 30 seconds preview mousing over the covers
- Creation of a playlist with all the songs
- Database storage for future data inquiries

# Missing
- Creation of users to consult search history
- Custom database searches:
    - Get all the tracks played by a deejay
    - Get all dj sets where a specific song / artist appears
    
# How it works
- Read the comments, description and "music in this video" to get the tracklist
- Search for the songs in Spotify and check of the results
- Storage of all data in the database

Technology used: Python, Flask, MySQL, AWS (Elastic Beanstalk), HTML, Javascript, REST API
