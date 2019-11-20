$('.tracks-btn').on('click', () => {
    const playlist_id = $(this).val()
    $.get('/playlist_tracks', playlist_id, (response) => {
        $('.playlist_id').html(response.tracks);
    });
});