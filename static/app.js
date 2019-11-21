$('.tracks-btn').on('dblclick', (evt) => {
    evt.preventDefault();
    const playlist_id = $(this).attr(value);
    console.log(playlist_id);

    $.get('/playlist-tracks', {'pl':playlist_id}, (tracks) => {
        console.log(tracks);
        for (track of tracks) {
            $(`.${playlist_id} ul`).append(`<li><a href="/tracks/${track.track_id}">${track.track_name}</a></li>`);
        }
    });
});