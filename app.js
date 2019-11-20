$('.playlist-tracks').on('click', () => {
    $.get('/playlist_tracks', (response) => {
        $('.modal').text(response);
    });
});