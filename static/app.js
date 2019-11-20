$('.tracks-btn').on('click', (evt) => {
    evt.preventDefault();
    const playlist_id = $(this).attr(value);
    console.log(playlist_id);

    $.get('/playlist-tracks', {'pl':playlist_id}, (res) => {
        $(`.${playlist_id}`).html(res.tracks);;
    });
});