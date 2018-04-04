module.exports = function(grunt) {
    // Project config
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        // Task configuration
        concat: {
            app: {
                src: ['caas/static/js/app/**/*.js'],
                dest: 'caas/static/js/app.js'
            },
            vendor: {
                src: ['caas/static/js/vendor/**/*.js'],
                dest: 'caas/static/js/lib.js'
            }
        }

        uglify: {
            app: {
                files: {'caas/static/js/app.min.js': ['caas/static/js/app/**/*.js']}
            },
            vendor: {
                files: {'caas/static/js/lib.min.js': ['caas/static/js/vendor/**/*.js']}
            }
        }

        sass: {
            dev: {
                options: {
                    includePaths: []
                },
                files: {
                    'caas/static/css/base.css': 'caas/static/scss/base.scss'
                }
            },
            deploy: {
                options: {
                    includePaths: [],
                    outputStyle: 'compressed'
                },
                files: {
                    'caas/static/css/base.min.css': 'caas/static/scss/base.scss'
                }
            }
        }

        watch: {
            options: {livereload: true}
            javascript: {
                files: ['caas/static/js/app/**/*.js'],
                tasks: ['concat']
            },
            sass: {
                files: 'caas/static/scss/**/*.scss',
                tasks: ['sass:dev']
            }
        }
    });

    // Load plugins.
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // Register tasks
    grunt.registerTask('default', []);
}