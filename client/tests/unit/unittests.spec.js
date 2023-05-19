import { shallowMount, mount } from '@vue/test-utils';
import App from '@/App.vue';
import TrackList from '@/components/TrackList.vue';
import Player from '@/components/Player.vue';
import EditProfile from '@/views/EditProfile.vue';
import Index from '@/views/Index.vue';
import Login from '@/views/Login.vue';
import NotFound from '@/views/NotFound.vue';
import Playlist from '@/views/Playlist.vue';
import Profile from '@/views/Profile.vue';
import Register from '@/views/Register.vue';
import Search from '@/views/Search.vue';

require('jest-fetch-mock').enableMocks()

beforeEach(() => {
  fetch.resetMocks();
});

class LocalStorageMock {
  constructor() {
    this.store = {};
  }

  clear() {
    this.store = {};
  }

  getItem(key) {
    return this.store[key] || null;
  }

  setItem(key, value) {
    this.store[key] = String(value);
  }

  removeItem(key) {
    delete this.store[key];
  }
}
global.localStorage = new LocalStorageMock;

describe('App.vue', () => {
  test('renders app', () => {
    fetch.mockResponse(JSON.stringify({"playlists": [{"name":"1", "tracks": [{"title": "bruh", "youtube_id": "bruh"}]}]}));
    const wrapper = shallowMount(App);
    expect(wrapper.text()).toContain('Login');
    
    expect(wrapper.find('nav.header-nav li:nth-child(1)').text()).toBe('Register');
    expect(wrapper.find('nav.header-nav li:nth-child(2)').text()).toBe('Login');
    expect(wrapper.find('nav.header-nav li:nth-child(3)').exists()).toBe(false);
    expect(wrapper.find('nav.header-nav li:nth-child(4)').exists()).toBe(false);
    
    expect(wrapper.find('.logo-name img').attributes('alt')).toBe('Logo');
    expect(wrapper.find('.logo-name h1').text()).toBe('Playlists');

    wrapper.vm.logged = true;
    wrapper.vm.$nextTick(() => {
      expect(wrapper.find('nav.header-nav li:nth-child(1)').text()).toBe('Profile');
      expect(wrapper.find('nav.header-nav li:nth-child(2)').text()).toBe('Logout');
    });
  });
});

describe('Register.vue', () => {
  test('contains register text', () => {
    const wrapper = shallowMount(Register);
    expect(wrapper.text()).toContain('Register');

  });
  it('should set username, password, confirmPassword, and role correctly when input values change', async () => {
    const wrapper = shallowMount(Register);

    const usernameInput = wrapper.find('input[type="text"]');
    const passwordInput = wrapper.find('input[type="password"]');
    const confirmPasswordInput = wrapper.findAll('input[type="password"]').at(1);
    const roleSelect = wrapper.find('select');

    await usernameInput.setValue('testuser');
    await passwordInput.setValue('password123');
    await confirmPasswordInput.setValue('password123');
    await roleSelect.setValue('admin');

    expect(wrapper.vm.username).toBe('testuser');
    expect(wrapper.vm.password).toBe('password123');
    expect(wrapper.vm.confirmPassword).toBe('password123');
    expect(wrapper.vm.role).toBe('admin');
  });

  it('should not submit when any required field is missing', async () => {
    const wrapper = shallowMount(Register);

    const registerButton = wrapper.find('.form-button');

    await registerButton.trigger('click');

    expect(fetchMock).not.toHaveBeenCalled();
  });
})

describe('TrackList.vue', () => {
  test('bruh in tracks', () => {
    const wrapper = shallowMount(TrackList, {
      propsData: {
      tracks: [{
          title: 'bruh',
          youtube_id: 'bruh',
        },
        {
          title: 'bruh2',
          youtube_id: 'bruh2',
        },
        {
          title: 'bruh3',
          youtube_id: 'bruh3',
        }],
      },
    });
    expect(wrapper.text()).toContain('bruh');
    expect(wrapper.findAll('.song')).toHaveLength(3);
  });
});


describe('Player.vue', () => {
  test('player button', () => {
    const wrapper = shallowMount(Player);
    expect(wrapper.text()).toContain('00:00');
    expect(wrapper.find("#play").exists()).toBe(true);
    expect(wrapper.vm.formatTime(75)).toBe('01:15');
    wrapper.vm.playing = true;
    wrapper.vm.$nextTick(() => {
      expect(wrapper.find('.play-pause').text()).toBe('pause');
    });
    expect(wrapper.vm.duration).toBe(0);
    expect(wrapper.vm.currentTime).toBe(0);
    expect(wrapper.vm.playing).toBe(true);
    expect(wrapper.vm.player).toBe(null);
  });
  
})

describe('Profile.vue', () => {
  test('contains profile', () => {
    fetch.mockResponseOnce(JSON.stringify({}));
    const $route = {
      fullPath: '/profile',
      params: { id: 1 }
    }
    const wrapper = mount(Profile, { 
      mocks: {
        $route
      } 
    })
    expect(wrapper.text()).toContain('Profile');
  });
  it('should set data properties correctly when created', async () => {
    fetch.mockResponseOnce(JSON.stringify({}));
    const $route = {
      fullPath: '/profile',
      params: { id: 1 }
    }
    const wrapper = mount(Profile, { 
      mocks: {
        $route
      } 
    })

    expect(wrapper.vm.role).toBe('');
    expect(wrapper.vm.username).toBe('');
    expect(wrapper.vm.playlists).toEqual([]);
    expect(wrapper.vm.id).toBe(null);
    expect(wrapper.vm.ownProfile).toBe(false);
    expect(wrapper.vm.iAdmin).toBe(false);
    expect(wrapper.vm.creatingPlaylist).toBe(false);
    expect(wrapper.vm.name).toBe('');
    expect(wrapper.vm.isPublic).toBe(false);
  });
})

describe('Login', () => {
  let wrapper;
  
  it('should set username and password correctly when input values change', async () => {
    wrapper = shallowMount(Login);
    fetch.mockResponse(JSON.stringify({}));
    const usernameInput = wrapper.find('#username');
    const passwordInput = wrapper.find('#password');

    await usernameInput.setValue('testuser');
    await passwordInput.setValue('password123');

    expect(wrapper.vm.username).toBe('testuser');
    expect(wrapper.vm.password).toBe('password123');
  });

  it('should not submit when username or password is empty', async () => {
    wrapper = shallowMount(Login);
    fetch.mockResponse(JSON.stringify({}));
    await wrapper.find('.form-button').trigger('click');

    expect(fetchMock).not.toHaveBeenCalled();
    expect(wrapper.emitted().login).toBeFalsy();
  });

});

describe('EditProfile.vue', () => {
  let wrapper;
  let fetchMock;
  let alertMock;
  let localStorageMock;

  beforeEach(() => {

    alertMock = jest.spyOn(window, 'alert');
    alertMock.mockImplementation(() => {});

    localStorageMock = {
      getItem: jest.fn(() => 'token123'),
    };
    global.localStorage = localStorageMock;

    wrapper = shallowMount(EditProfile);
  });

  afterEach(() => {
    wrapper.destroy();
    jest.clearAllMocks();
  });

  it('should set password, username, newPassword, and newPasswordConfirm correctly when input values change', async () => {
    const passwordInput = wrapper.find('input[type="password"]');
    const usernameInput = wrapper.find('input[type="text"]');
    const newPasswordInput = wrapper.findAll('input[type="password"]').at(1);
    const newPasswordConfirmInput = wrapper.findAll('input[type="password"]').at(2);

    await passwordInput.setValue('oldpassword');
    await usernameInput.setValue('newusername');
    await newPasswordInput.setValue('newpassword');
    await newPasswordConfirmInput.setValue('newpassword');

    expect(wrapper.vm.password).toBe('oldpassword');
    expect(wrapper.vm.username).toBe('newusername');
    expect(wrapper.vm.newPassword).toBe('newpassword');
    expect(wrapper.vm.newPasswordConfirm).toBe('newpassword');
  });

  it('should not submit when password is empty', async () => {
    await wrapper.find('.form-button').trigger('click');

    expect(alertMock).not.toHaveBeenCalled();
  });
})

describe('Playlist.vue', () => {
  test('contains playlist component', () => {
    fetch.mockResponseOnce(JSON.stringify({"name":"Playlist"}));
    const $route = {
      fullPath: '/playlist',
      params: { id: 1 }
    }
    const wrapper = mount(Playlist, { 
      mocks: {
        $route
      } 
    })
    expect(wrapper.text()).toContain('Playlist');
  });
  it('should set data properties correctly when created', async () => {
    fetch.mockResponseOnce(JSON.stringify({"name":"Playlist"}));
    const $route = {
      fullPath: '/playlist',
      params: { id: 1 }
    }
    const wrapper = mount(Playlist, { 
      mocks: {
        $route
      } 
    })

    expect(wrapper.vm.name).toBe('Playlist');
    expect(wrapper.vm.tracks).toEqual([]);
    expect(wrapper.vm.isMine).toBe(false);
    expect(wrapper.vm.editingPlaylist).toBe(false);
    expect(wrapper.vm.editedName).toBe('');
    expect(wrapper.vm.isPublic).toBe(false);
    expect(wrapper.vm.id).toBe(null);
  });
})

describe('Search.vue', () => {
  test('contains search component', () => {
    fetch.mockResponse(JSON.stringify({}));
    const $route = {
      fullPath: '/search',
      params: { query: "bruh" }
    }
    const wrapper = mount(Search, { 
      mocks: {
        $route
      } 
    })
    expect(wrapper.text()).toContain('Search');
  });
  it('should set data properties correctly when created', async () => {
    fetch.mockResponse(JSON.stringify({}));
    const $route = {
      fullPath: '/search',
      params: { query: "bruh" }
    }
    const wrapper = mount(Search, { 
      mocks: {
        $route
      } 
    })

    expect(wrapper.vm.tracks).toEqual([]);
    expect(wrapper.vm.playlists).toEqual([]);
    expect(wrapper.vm.users).toEqual([]);
  });
})

describe('Index.vue', () => {
  test('index', () => {
    const wrapper = shallowMount(Index);
    expect(wrapper.text()).toContain('');
  });
})


describe('NotFound.vue', () => {
  test('404 page', () => {
    const wrapper = shallowMount(NotFound);
    expect(wrapper.text()).toContain('404');
  });
})



