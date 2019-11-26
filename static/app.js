$(document).ready(function() {  // Load all html elems before adding evt handlers
    const tracksBtn = $('.tracks-btn');

    // Get tracks from a playlist and display in a modal
    tracksBtn.on('click', (evt) => {
        evt.preventDefault();
        const playlist_id = evt.target.value;

        // Get playlist tracks and add to modal
        $.get('/playlist-tracks', {'pl':playlist_id}, (tracks) => {
            for (track of tracks) {
                $(`.${playlist_id} ul`).append(`<li><a href="/tracks/${track.track_id}">${track.track_name}</a></li>`);
            }
        });

        // Close modal upon click
        const closeBtn = $(`#close-btn-${playlist_id}`);
        closeBtn.on('click', (e) => {
            e.preventDefault();
            console.log('hi')
            modal.toggle('show-modal');
        });

        // Display the modal
        const modal = $(`#modal-${playlist_id}`);
        modal.toggle('show-modal');
    });

    // Remove track from page when user clicks X
    const deselectBtn = $('.deselect');
    deselectBtn.on('click', (evt) => {
        evt.preventDefault();
        const track_id = evt.target.value;
        $(`#deselect-${track_id}-div`).remove();  // Remove X button
        // $(`#track-href-${track_id}`).remove();  // Remove track info
    });



    // Submit new playlist
    const createPlaylistBtn = $('#create-pl');
    createPlaylistBtn.on('click', (evt) => {
        evt.preventDefault();
        const pl_name = $('#new-pl-name').html();  // Get playlist name
        const tracks = $('.add-track');
        console.log(tracks);
        for (track of tracks) {
            console.log(track.val());
        }
    });
})