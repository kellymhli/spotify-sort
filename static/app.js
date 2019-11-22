$(document).ready(function() {
    const tracksBtn = $('.tracks-btn')

    tracksBtn.on('click', (evt) => {
        evt.preventDefault();
        const playlist_id = evt.target.value;

        $.get('/playlist-tracks', {'pl':playlist_id}, (tracks) => {
            for (track of tracks) {
                $(`.${playlist_id} ul`).append(`<li><a href="/tracks/${track.track_id}">${track.track_name}</a></li>`);
            }
        });

        const modal = $(`#modal-${playlist_id}`)
        modal.toggle('show-modal');

        const closeBtn = $(`#close-btn-${playlist_id}`)
        closeBtn.on('click', (evt) => {
            modal.toggle('show-modal');
        });
    });
})