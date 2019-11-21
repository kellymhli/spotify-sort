$(document).ready(function(){  // Load page before adding event handlers

    // Create event listener on tracks bottons
    $('.tracks-btn').on('click', (evt) => {
        evt.preventDefault();
        const playlist_id = evt.target.value;
        $.get('/playlist-tracks', {'pl':playlist_id}, (tracks) => {
            // console.log(tracks);
            for (track of tracks) {
                $(`.${playlist_id} ul`).append(`<li><a href="/tracks/${track.track_id}">${track.track_name}</a></li>`);
            }
        });
    })
})