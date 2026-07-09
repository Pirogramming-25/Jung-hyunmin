function getCookie(name) {
  const match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return match ? match.pop() : '';
}

async function postJSON(url) {
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Accept': 'application/json',
    },
  });
  return res.json();
}

function toggleLike(btn, postId) {
  postJSON(`/api/posts/${postId}/like/`).then(data => {
    btn.classList.toggle('active', data.liked);
    const countEl = document.getElementById(`likes-count-${postId}`);
    if (countEl) countEl.textContent = `좋아요 ${data.likes_count}`;
  });
}

function toggleBookmark(btn, postId) {
  postJSON(`/api/posts/${postId}/bookmark/`).then(data => {
    btn.classList.toggle('active', data.bookmarked);
  });
}

function toggleFollow(btn, username) {
  postJSON(`/api/users/${username}/follow/`).then(data => {
    btn.textContent = data.following ? '팔로잉' : '팔로우';
    btn.classList.toggle('following', data.following);
  });
}

async function postJSONBody(url, body) {
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
      'Accept': 'application/json',
    },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, data };
}

function flattenErrors(data) {
  if (!data || typeof data !== 'object') return '요청에 실패했습니다.';
  return Object.values(data).flat().join(' ') || '요청에 실패했습니다.';
}

async function patchJSONBody(url, body) {
  const res = await fetch(url, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
      'Accept': 'application/json',
    },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, data };
}

async function deleteResource(url, redirectTo) {
  if (!confirm('삭제하시겠습니까?')) return;
  const res = await fetch(url, {
    method: 'DELETE',
    headers: { 'X-CSRFToken': getCookie('csrftoken') },
  });
  if (res.ok) {
    if (redirectTo) window.location.href = redirectTo;
    else location.reload();
  } else {
    alert('삭제에 실패했습니다.');
  }
}

function toggleEdit(key) {
  document.getElementById(`view-${key}`).style.display = 'none';
  document.getElementById(`edit-${key}`).style.display = 'flex';
}

function cancelEdit(key) {
  document.getElementById(`view-${key}`).style.display = '';
  document.getElementById(`edit-${key}`).style.display = 'none';
}

async function saveCommentEdit(id) {
  const input = document.getElementById(`edit-input-comment-${id}`);
  const { ok } = await patchJSONBody(`/api/comments/${id}/`, { content: input.value });
  if (ok) location.reload();
  else alert('수정에 실패했습니다.');
}

async function savePostCaption(id) {
  const input = document.getElementById(`edit-input-caption-${id}`);
  const { ok } = await patchJSONBody(`/api/posts/${id}/`, { caption: input.value });
  if (ok) location.reload();
  else alert('수정에 실패했습니다.');
}

async function handleLoginSubmit(event, form) {
  event.preventDefault();
  const errorEl = form.querySelector('.form-error');
  errorEl.textContent = '';
  const { ok, data } = await postJSONBody('/api/login/', {
    username: form.username.value,
    password: form.password.value,
  });
  if (ok) {
    window.location.href = '/';
  } else {
    errorEl.textContent = data.error || flattenErrors(data);
  }
}

async function handleSignupSubmit(event, form) {
  event.preventDefault();
  const errorEl = form.querySelector('.form-error');
  errorEl.textContent = '';
  const { ok, data } = await postJSONBody('/api/signup/', {
    username: form.username.value,
    password: form.password.value,
    password2: form.password2.value,
    name: form.name.value,
    email: form.email.value,
  });
  if (ok) {
    window.location.href = '/';
  } else {
    errorEl.textContent = flattenErrors(data);
  }
}

async function handleCreatePostSubmit(event, form) {
  event.preventDefault();
  const errorEl = form.querySelector('.form-error');
  errorEl.textContent = '';

  if (!form.images.files.length) {
    errorEl.textContent = '이미지를 1장 이상 선택해주세요.';
    return;
  }

  const formData = new FormData();
  formData.append('caption', form.caption.value);
  for (const file of form.images.files) {
    formData.append('images', file);
  }

  const res = await fetch('/api/posts/', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Accept': 'application/json' },
    body: formData,
  });
  const data = await res.json().catch(() => ({}));
  if (res.ok) {
    window.location.href = form.dataset.redirect || '/';
  } else {
    errorEl.textContent = flattenErrors(data);
  }
}

async function handleAddComment(event, form, postId) {
  event.preventDefault();
  const errorEl = form.parentElement.querySelector('.comment-error');
  errorEl.textContent = '';
  const { ok, data } = await postJSONBody('/api/comments/', {
    post: postId,
    content: form.content.value,
  });
  if (ok) {
    location.reload();
  } else {
    errorEl.textContent = flattenErrors(data);
  }
}

async function handleCreateStorySubmit(event, form) {
  event.preventDefault();
  const errorEl = form.querySelector('.form-error');
  errorEl.textContent = '';

  if (!form.images.files.length) {
    errorEl.textContent = '이미지를 1장 이상 선택해주세요.';
    return;
  }

  const formData = new FormData();
  for (const file of form.images.files) {
    formData.append('images', file);
  }

  const res = await fetch('/api/stories/', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Accept': 'application/json' },
    body: formData,
  });
  const data = await res.json().catch(() => ({}));
  if (res.ok) {
    window.location.href = form.dataset.redirect || '/';
  } else {
    errorEl.textContent = flattenErrors(data);
  }
}
