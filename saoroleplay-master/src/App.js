import React from 'react'
import { Route, Switch } from 'react-router-dom'
// We will create these two pages in a moment
import chat from './chat/chat.js';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function App() {
  return (
    <Switch>
      <Route exact path="/" component={chat} />
    </Switch>
  )
}