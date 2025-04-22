import { createRouter, createWebHistory } from 'vue-router';
import Login from '../pages/Login.vue';
import DashboardAdmin from '../pages/DashboardAdmin.vue';
import ManageUsers from '../pages/ManageUsers.vue';
import Students from '../pages/Students.vue';
import UploadSample from '../pages/UploadSample.vue';
import UploadAssignment from '../pages/UploadAssignment.vue';
import History from '../pages/History.vue';
// import VerifyTask from '../pages/VerifyTask.vue';
// import VerificationLogs from '../pages/VerificationLogs.vue';
// import Notifications from '../pages/Notifications.vue';
// import Logout from '../pages/Logout.vue';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/dashboard', component: DashboardAdmin },
  { path: '/manajemen-pengguna', component: ManageUsers },
  { path: '/data-siswa', component: Students },
  { path: '/upload-sample', component: UploadSample },
  { path: '/upload-tugas', component: UploadAssignment },
  { path: '/history', component: History },
//   { path: '/verify', component: VerifyTask },
//   { path: '/logs', component: VerificationLogs },
//   { path: '/notifications', component: Notifications },
//   { path: '/logout', component: Logout },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('access_token');
  
    if (!token && to.path !== '/login') {
      next('/login'); // Redirect ke login jika belum login
    } else {
      next();
    }
  });
  

export default router;
