$(document).ready(function(){  // Load page before adding event handlers

    // Create event listener on tracks bottons
    $('.tracks-btn').on('click', (evt) => {
        evt.preventDefault();
        const playlist_id = evt.target.value;

        $.get('/playlist-tracks', {'pl':playlist_id}, (tracks) => {
            for (track of tracks) {
                $(`.${playlist_id} ul`).append(`<li><a href="/tracks/${track.track_id}">${track.track_name}</a></li>`);
            }
        });
        
        const modal = $(`#modal-${playlist_id}`)
        const modalOverlay = $(`#modal-overlay-${playlist_id}`)
        const closeBtn = $(`close-btn-${playlist_id}`)

        modal.classList.toggle('closed');
        modalOverlay.classList.toggle('closed');
    })

})