document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit').forEach(editButton => {
        editButton.addEventListener('click', function() {
            let post = this.closest('.posts');
            if (post) {
                post.querySelector('.postEdit').style.display = 'block';
                post.querySelector('.postEditButton').style.display = 'block';
                post.querySelector('.postContent').style.display = 'none';
                post.querySelector('.edit').style.display = 'none';
            }
        })
    });

    const likeButtons = document.querySelectorAll('.postLikes');

    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.postId;
            toggleLike(postId, this);
        });
    });

    function toggleLike(postId, button) {
        fetch(`/api/toggle-like/${postId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            button.textContent = data.liked ? `${data.like_count--}` : data.like_count++;
        });
    }

    document.querySelectorAll('.postLikes').forEach(editButton => {
        editButton.addEventListener('click', function() {
            let post = this.closest('.posts');
            if (post) {
                let emptyHeart = post.querySelector('#emptyheart');
                let fullHeart = post.querySelector('#fullheart');

                let emptyHeartDisplayStyle = window.getComputedStyle(emptyHeart).getPropertyValue('display');

                if (emptyHeartDisplayStyle === 'block') {
                    emptyHeart.style.display = 'none';
                    fullHeart.style.display = 'block';
                } else {
                    emptyHeart.style.display = 'block';
                    fullHeart.style.display = 'none';
                }
            }
        })
    });
});

