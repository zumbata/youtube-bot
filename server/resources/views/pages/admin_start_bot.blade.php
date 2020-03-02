@extends('layouts.default', ['title' => 'Choose Bot'])
@section('content')
    <div class="row justify-content-center text-center">
        <div class="mt-5 rounded-pill col-6 col-color">
            <h3 class="mt-2">Choose which bot to operate</h3>
            @if(isset($success) && $success == true)
            <p class="text-success">Bot started successfully.</p>
            @endif
            <div class="row my-3">
                <div class="col-6">
                    <a class="btn btn-primary text-uppercase" href="/admin/bot/old">Old Bot</a>
                </div>
                <div class="col-6">
                    <a class="btn btn-primary text-uppercase" href="/admin/bot/new">New Bot</a>
                </div>
            </div>
        </div>
    </div>
@stop