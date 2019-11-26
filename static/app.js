$(document).ready(function() {  // Load all html elems before adding evt handlers
    const tracksBtn = $('.tracks-btn');

    // Get tracks from a playlist and display in a modal
    tracksBtn.on('click', (evt) => {
        evt.preventDefault();
        const playlistId = evt.target.value;

        // Get playlist tracks and add to modal
        $.get('/playlist-tracks', {'pl':playlistId}, (tracks) => {
            for (track of tracks) {
                $(`.${playlistId} ul`).append(`<li><a href="/tracks/${track.track_id}">${track.track_name}</a></li>`);
            }
        });

        // Close modal upon click
        const closeBtn = $(`#close-btn-${playlistId}`);
        closeBtn.on('click', (e) => {
            e.preventDefault();
            console.log('hi')
            modal.toggle('show-modal');
        });

        // Display the modal
        const modal = $(`#modal-${playlistId}`);
        modal.toggle('show-modal');
    });

    // Remove track from page when user clicks X
    const deselectBtn = $('.deselect');
    deselectBtn.on('click', (evt) => {
        evt.preventDefault();
        const trackId = evt.target.value;
        $(`#deselect-${trackId}-div`).remove();
    });

    // Submit new playlist
    const createPlaylistBtn = $('#create-pl');
    createPlaylistBtn.on('click', (evt) => {
        evt.preventDefault();
        trackIds = [];
        const plName = $('#new-pl-name').html();  // Get playlist name
        const trackDivs = $('.add-track-div');

        for (track of trackDivs) {
            console.log(track);
            console.log(track.attr('value'));
        };
    });
})