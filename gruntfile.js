module.exports = function (grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        concat: {
            options: {
                separator: ''
            },
            js: {
                src: ['vendors/sufee-admin-dashboard/vendors/jquery/dist/jquery.min.js',
                    'vendors/sufee-admin-dashboard/vendors/popper.js/dist/umd/popper.min.js',
                    'vendors/sufee-admin-dashboard/vendors/bootstrap/dist/js/bootstrap.min.js',
                    'vendors/sufee-admin-dashboard/assets/js/main.js',
                    'vendors/sufee-admin-dashboard/vendors/chart.js/dist/Chart.bundle.min.js',
                    'vendors/sufee-admin-dashboard/assets/js/dashboard.js',
                    'vendors/sufee-admin-dashboard/assets/js/widgets.js',
                    'vendors/sufee-admin-dashboard/vendors/jqvmap/dist/jquery.vmap.min.js',
                    'vendors/sufee-admin-dashboard/vendors/jqvmap/examples/js/jquery.vmap.sampledata.js',
                    'vendors/sufee-admin-dashboard/vendors/jqvmap/dist/maps/jquery.vmap.world.js',
                    'static/script.js'],
                dest: 'static/script.min.js'
            },

            css: {
                src: [
                    'vendors/sufee-admin-dashboard/vendors/bootstrap/dist/css/bootstrap.min.css',
                    'vendors/sufee-admin-dashboard/vendors/font-awesome/css/font-awesome.min.css',
                    'vendors/sufee-admin-dashboard/vendors/themify-icons/css/themify-icons.css',
                    'vendors/sufee-admin-dashboard/vendors/flag-icon-css/css/flag-icon.min.css',
                    'vendors/sufee-admin-dashboard/vendors/selectFX/css/cs-skin-elastic.css',
                    'vendors/sufee-admin-dashboard/vendors/jqvmap/dist/jqvmap.min.css',
                    'vendors/sufee-admin-dashboard/assets/css/style.css',
                    'static/style.css'
                ],
                dest: 'static/style.min.css'
            }
        },

        uglify: {
            options: {
                banner: '/* This file is auto-generated. Please don\'t modify it! */'
            },
            js: {
                files: {
                    'static/script.min.js': ['static/script.min.js']
                }
            }

        },

        cssmin: {
            css: {
                files: {
                    'static/style.min.css': ['static/style.min.css']
                }
            }
        },

        copy: {
            fonts: {
                cwd: 'vendors/sufee-admin-dashboard/vendors/font-awesome/fonts',
                src: '**/*',
                dest: 'fonts/',
                expand: true
            },
        },

    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-uglify-es');
    grunt.loadNpmTasks('grunt-contrib-copy');

    grunt.registerTask('default', ['js', 'css', 'copy:fonts']);
    grunt.registerTask('js', ['concat:js', 'uglify:js']);
    grunt.registerTask('css', ['concat:css', 'cssmin:css']);
};
