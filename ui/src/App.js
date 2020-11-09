import React, { Component } from 'react'
import { BrowserRouter, Route, Switch } from 'react-router-dom'
import { createBrowserHistory } from 'history'
import RPGManagerView from './pages/rpgmanager/RPGManagerView'
import PageNotFound from './pages/common/PageNotFound'


export default class App extends Component {
    history = createBrowserHistory()

    render() {
        return (
            <BrowserRouter>
                <Switch>
                    <Route exact path='/' component={RPGManagerView} />
                    <Route path='/rpgmanager/:id' component={RPGManagerView} />
                    <Route path='/rpgmanager' component={RPGManagerView} />
                    <Route component={PageNotFound} />
                </Switch>
            </BrowserRouter>
        )
    }
}
